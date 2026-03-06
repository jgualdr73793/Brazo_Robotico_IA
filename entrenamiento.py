from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from Venv_Brazo import BrazoEnv

# crear un entorno paralelo(es mas rapido para entrenamientos)
env=make_vec_env(BrazoEnv, n_envs=4)

# Crear el modelo PPO
model=PPO("MlpPolicy", env, verbose=1)

# Entrenar( El ajuste puede variar dependiendo de la gama del dispositivo)
model.learn(total_timesteps=100000)

# Guardar
model.save("Brazo_ppo")

print("Entrenamiento Completado") 
