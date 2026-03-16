import gymnasium as gym
from gymnasium import spaces
import pybullet as p
import pybullet_data
import numpy as np

class BrazoEnv(gym.Env):
    def __init__(self, render=False):
        super().__init__()
        self.client = p.connect(p.GUI if render else p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        
        self.num_joints = 5
        self.max_steps = 1200 # Más tiempo para maniobrar
        self.current_step = 0
        
        self.action_space = spaces.Box(low=-1, high=1, shape=(self.num_joints,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(11,), dtype=np.float32)
        
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        p.setTimeStep(1./500.) 
        
        p.loadURDF("plane.urdf")
        # Asegúrate de tener tu urdf de 50cm en la carpeta urdf/
        self.robot_id = p.loadURDF("../urdf/mi_brazo.urdf", [0, 0, 0], useFixedBase=True)
        self.ball_id = -1

        # Filtro de colisiones interno para que no se trabe consigo mismo
        p.setCollisionFilterPair(self.robot_id, self.robot_id, 1, 2, enableCollision=0)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0 
        for i in range(self.num_joints):
            p.resetJointState(self.robot_id, i, targetValue=0)
        
        # Objetivo Aleatorio: Frente al brazo, a distintas alturas
        self.target_pos = np.array([
            np.random.uniform(0.15, 0.35),
            np.random.uniform(-0.25, 0.25),
            np.random.uniform(0.10, 0.40)
        ])

        if self.ball_id != -1:
            p.removeBody(self.ball_id)
            
        # Bola Fantasma: Solo visual, sin colisión física
        v_id = p.createVisualShape(p.GEOM_SPHERE, radius=0.03, rgbaColor=[0, 1, 0, 0.7])
        self.ball_id = p.createMultiBody(
            baseMass=0,
            baseVisualShapeIndex=v_id, 
            baseCollisionShapeIndex=-1, 
            basePosition=self.target_pos
        )

        return self._get_obs(), {}

    def step(self, action):
        self.current_step += 1
        
        # 1. CONTROL RELATIVO (DELTAS)
        for i in range(self.num_joints):
            estado_actual = p.getJointState(self.robot_id, i)[0]
            delta = action[i] * 0.2  # Maximo 0.2 radianes por paso (~11 grados)
            target_ang = estado_actual + delta
            
            # Limite físico para que no se enrosque sobre sí mismo (90 grados max por lado)
            target_ang = np.clip(target_ang, -1.57, 1.57) 
            
            p.setJointMotorControl2(
                bodyUniqueId=self.robot_id, 
                jointIndex=i, 
                controlMode=p.POSITION_CONTROL, 
                targetPosition=target_ang, 
                force=200,
                maxVelocity=3.0,
                positionGain=0.1,
                velocityGain=1.0
            )
        
        for _ in range(2): p.stepSimulation()

        # 2. LECTURA DE POSICIONES
        state_punta = p.getLinkState(self.robot_id, 5) # Punta final
        pos_punta = np.array(state_punta[0])
        distancia = np.linalg.norm(pos_punta - self.target_pos)

        # Alturas de los eslabones para la "Postura de Grúa"
        # link 1 es el codo, link 2 es la muñeca base
        z_codo = p.getLinkState(self.robot_id, 1)[0][2]
        z_muneca = p.getLinkState(self.robot_id, 2)[0][2]
        
        # 3. EL SISTEMA DE RECOMPENSAS (Zanahoria y Garrote Industrial)
        reward = -10.0 * distancia             # ¡Duele estar lejos!
        reward += 1.0 / (distancia + 0.1)      # ¡Magnético al acercarse!

        # Postura Anti-Suelo
        min_z = min(z_codo, z_muneca, pos_punta[2])
        if min_z < 0.05:
            reward -= 5.0  # Castigo severo por arrastrarse

        # Postura de Grúa (Hombro alto)
        if z_codo > 0.15:
            reward += 1.0  # Premio por mantener la estructura alta

        # Eficiencia Energética
        reward -= 0.01 * np.sum(np.square(action)) 
        reward -= 0.05 * abs(action[1]) # Penalización extra por mover mucho el hombro

        # 4. TERMINACIÓN ESTRICTA
        terminated = False
        if distancia < 0.03:
            reward += 100.0 # ¡Llegó al centro!
            terminated = True
            
        truncated = self.current_step >= self.max_steps
        return self._get_obs(), reward, terminated, truncated, {}

    def _get_obs(self):
        j_states = p.getJointStates(self.robot_id, range(self.num_joints))
        j_poses = np.array([s[0] for s in j_states], dtype=np.float32) / 3.1416
        s_punta = p.getLinkState(self.robot_id, 5)
        pos_p = np.array(s_punta[0], dtype=np.float32)
        err = (self.target_pos - pos_p).astype(np.float32)
        return np.concatenate([j_poses, pos_p, err]).astype(np.float32)

    def close(self):
        p.disconnect()