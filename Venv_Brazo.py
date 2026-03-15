import gymnasium as gym
import numpy as np
import pybullet as p 
import pybullet_data
import time

class BrazoEnv(gym.Env):
    def __init__(self, render=False):
        super().__init__()
        self.render_mode = render
        
        # Conexión inicial
        self.physics_client = p.connect(p.GUI if render else p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        
        # Parámetros del robot
        self.num_joints = 5 
        
        # Espacio de Acciones: -1 a 1 para los 5 motores
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(self.num_joints,), dtype=np.float32)
        
        # Espacio de Observación: 
        # [5 posiciones joints + 5 velocidades joints + 3 coordenadas objetivo XYZ] = 13 total
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(13,), dtype=np.float32)

        self.step_count = 0
        self.max_steps = 500
        self.prev_action = np.zeros(self.num_joints)
        self.target_pos = np.array([0.3, 0.0, 0.3]) # Posición inicial por defecto

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        p.loadURDF("plane.urdf")
        
        # Cargar robot
        self.robot_id = p.loadURDF("urdf/mi_brazo.urdf", [0, 0, 0], useFixedBase=True)
        
        # 1. Generar nuevo objetivo aleatorio en el plano alcanzable
        x = np.random.uniform(0.2, 0.45)
        y = np.random.uniform(-0.3, 0.3)
        z = np.random.uniform(0.15, 0.5)
        self.target_pos = np.array([x, y, z])

        # 2. Crear esfera visual roja para ver el objetivo
        visual_id = p.createVisualShape(p.GEOM_SPHERE, radius=0.03, rgbaColor=[1, 0, 0, 0.8])
        p.createMultiBody(baseVisualShapeIndex=visual_id, basePosition=self.target_pos)

        # 3. Reiniciar contadores y memoria de acciones
        self.step_count = 0
        self.prev_action = np.zeros(self.num_joints)

        return self._get_obs(), {}

    def step(self, action):
        # 1. Aplicar control de motores (Escalado a radianes)
        target_positions = action * 1.57 
        
        for i in range(self.num_joints):
            p.setJointMotorControl2(
                self.robot_id,
                i,
                p.POSITION_CONTROL,
                targetPosition=target_positions[i],
                force=250
            )
        
        p.stepSimulation()
        if self.render_mode:
            time.sleep(1./240.)

        # 2. Obtener estados actuales
        obs = self._get_obs()
        
        # Obtener posición real de la punta (Link 4)
        ee_state = p.getLinkState(self.robot_id, self.num_joints - 1)
        ee_pos = np.array(ee_state[0])

        # 3. CÁLCULO DE RECOMPENSA (Reward Engineering)
        distancia = np.linalg.norm(ee_pos - self.target_pos)
        
        # Recompensa base negativa (Max = 0)
        reward = -distancia 

        # Penalización por movimiento abrupto (Smoothness)
        abrupticidad = np.linalg.norm(action - self.prev_action)
        reward -= 0.1 * abrupticidad 

        # Penalización por energía (Esfuerzo cuadrático)
        energia = np.sum(np.square(action))
        reward -= 0.01 * energia

        # 4. Actualizar estado y verificar fin
        self.prev_action = action.copy()
        self.step_count += 1
        
        # Bonus por estar muy cerca
        if distancia < 0.05:
            reward += 0.5

        terminated = self.step_count >= self.max_steps
        truncated = False

        return obs, reward, terminated, truncated, {}

    def _get_obs(self):
        states = p.getJointStates(self.robot_id, range(self.num_joints))
        pos = np.array([s[0] for s in states], dtype=np.float32)
        vel = np.array([s[1] for s in states], dtype=np.float32)
        
        # Concatenamos todo para que la IA sepa dónde está y dónde está la meta
        return np.concatenate([pos, vel, self.target_pos.astype(np.float32)])

    def close(self):
        p.disconnect(self.physics_client)