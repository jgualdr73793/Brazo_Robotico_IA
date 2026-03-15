from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from Venv_Brazo import BrazoEnv
import torch

# 1. Crear entornos paralelos
# IMPORTANTE: Asegúrate de que BrazoEnv(render=False) sea el default
env = make_vec_env(lambda: BrazoEnv(render=False), n_envs=4)

# 2. Crear el modelo PPO con soporte para GPU
# Usamos 'device="cuda"' para que la RTX 4050 haga el trabajo pesado
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Entrenando en: {device}")

model = PPO(
    "MlpPolicy", 
    env, 
    verbose=1, 
    device=device,
    learning_rate=0.0003, # Tasa de aprendizaje estándar para robótica
    n_steps=2048          # Tamaño del buffer por cada entorno
)

# 3. Entrenar
# 100,000 pasos es un buen inicio para "ver" si entiende la lógica del XYZ
print("Iniciando entrenamiento del nuevo sistema XYZ...")
model.learn(total_timesteps=100000)

# 4. Guardar con un nombre que identifique el nuevo sistema
model.save("Brazo_ppo_xyz_v1")

print("Entrenamiento Completado y Guardado")