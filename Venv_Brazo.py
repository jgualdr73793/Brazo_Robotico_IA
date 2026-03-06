import gymnasium as gym
import numpy as np
import pybullet as p 
import pybullet_data
import time

class BrazoEnv(gym.Env):
	def __init__(self, render=False):

		super().__init__()
		self.render_mode = render
		self.physics_client= p.connect(p.GUI if render else p.DIRECT)
		p.setAdditionalSearchPath(pybullet_data.getDataPath())
		p.setGravity(0, 0, -9.81)
		p.loadURDF("plane.urdf")
	
		self.robot_id=p.loadURDF("urdf/mi_brazo.urdf",[0, 0, 0],useFixedBase=True)

		self.num_joints= 5 # 5 GRADOS DE LINERTAD

		self.action_space = gym.spaces.Box(low=-1, high=1, shape=(self.num_joints,),dtype=np.float32)
		self.observation_space=gym.spaces.Box(low=np.inf, high=np.inf, shape=(self.num_joints*2,), dtype=np.float32)

		self.target_angles = np.array([0.0, 0.5, -0.5, 0.0, 0.0])
		
		self.step_count = 0
		self.max_steps = 500

	def reset(self, seed=None, options=None):
		p.resetSimulation()
		p.setGravity(0, 0, -9.81)
		p.loadURDF("plane.urdf")
		self.robot_id=p.loadURDF("urdf/mi_brazo.urdf", [0,0,0], useFixedBase=True)
		self.step_count = 0
		return self._get_obs(), {}

	def step(self, action):
		target_positions = action * 1.57 #  Se escala desde -1/1 a -90°/90° aproximadamente
		
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
	
		obs = self._get_obs()
		reward = np.linalg.norm(obs[:self.num_joints] - self.target_angles)
		terminated = self.step_count >= self.max_steps
		self.step_count += 1

		return obs, reward, terminated , False, {}
	
	def _get_obs(self):
		states = p.getJointStates(self.robot_id, range(self.num_joints))
		pos = np.array([s[0] for s in states], dtype=np.float32)
		vel = np.array([s[1] for s in states], dtype=np.float32)
		return np.concatenate([pos,vel])		

	def close(self):
		p.disconnect(self.physics_client)
