from stable_baselines3 import PPO
from Venv_Brazo import BrazoEnv
import time

# Cargar el modelo entrenado
model=PPO.load("Brazo_ppo")

# Crear entorno con render (para poder ver la simulación)
env = BrazoEnv(render=True) #GUI activado

obs, _ = env.reset()
terminated = False
total_reward = 0

while not terminated:
	action, _ = model.predict(obs)
	obs, reward, terminated, truncated, info= env.step(action)
	total_reward += reward
	time.sleep(0.02)

print(f"Prueba Terminada. Recompensa total acumulada: {total_reward}")

env.close()
