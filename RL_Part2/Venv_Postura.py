import gymnasium as gym
from gymnasium import spaces
import pybullet as p
import pybullet_data
import numpy as np

class BrazoPosturaEnv(gym.Env):
    def __init__(self, render=False):
        super().__init__()

        # 1. Conexión
        self.client = p.connect(p.GUI if render else p.DIRECT)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        self.num_joints = 5
        self.max_steps = 1200
        self.current_step = 0

        # 2. Espacios (Normalizados -1 a 1)
        self.action_space = spaces.Box(low=-1, high=1, shape=(5,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-1, high=1, shape=(5,), dtype=np.float32)

        # 3. Mundo Físico
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        self.plane_id = p.loadURDF("plane.urdf")
        self.robot_id = p.loadURDF("../urdf/mi_brazo.urdf", [0, 0, 0], useFixedBase=True)

    def step(self, action):
        self.current_step += 1
        
        # 1. MOVIMIENTO (Lógica Negativa = Arriba)
        for i in range(self.num_joints):
            pos_actual = p.getJointState(self.robot_id, i)[0]
            # Paso de 0.15 para tener buena reacción
            nueva_pos = pos_actual + (action[i] * 0.15) 

            if i == 1: # HOMBRO
                # Clip de -1.6 (techo) a 0.0 (suelo)
                nueva_pos = np.clip(nueva_pos, -1.6, 0.0)
            else:
                nueva_pos = np.clip(nueva_pos, -3.14, 3.14)

            # Fuerza de 500 para que no sea un "fideo"
            p.setJointMotorControl2(
                bodyIndex=self.robot_id,
                jointIndex=i,
                controlMode=p.POSITION_CONTROL,
                targetPosition=nueva_pos,
                force=500.0
            )        
        
        p.stepSimulation()

        # 2. RECOMPENSA (Objetivo en -1.17 rad)
        angulo_hombro = p.getJointState(self.robot_id, 1)[0]
        
        # El error ahora se mide contra el valor negativo
        error = abs(angulo_hombro - (-1.17))

        # Recompensa Exponencial: Máximo 1.0 si llega a -1.17
        reward = float(np.exp(-3.0 * error))

        # 3. FINALIZACIÓN
        # Ya no usamos colisiones para que no se frustre si el resto del brazo toca el piso
        terminated = False
        truncated = self.current_step >= self.max_steps
        
        return self._get_obs(), reward, terminated, truncated, {}   

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0

        # Nacer ya levantado para "oler" los puntos rápido
        for i in range(self.num_joints):
            if i == 1:
                # Nace en la zona "buena" (entre -1.5 y -0.5)
                angulo_inicial = np.random.uniform(-1.5, -0.5)
            else:
                angulo_inicial = 0.0
                
            p.resetJointState(self.robot_id, i, angulo_inicial)
            # Sincronizamos el motor con la posición de reset
            p.setJointMotorControl2(self.robot_id, i, p.POSITION_CONTROL, targetPosition=angulo_inicial, force=0)

        return self._get_obs(), {}

    def _get_obs(self):
        estados = p.getJointStates(self.robot_id, range(5))
        angulos = [estado[0] for estado in estados]
        # Normalizamos dividiendo por PI
        return np.array(angulos, dtype=np.float32) / 3.1416
    
    def close(self):
        p.disconnect()