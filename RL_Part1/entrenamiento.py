import os
import torch
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecMonitor, SubprocVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from Venv_Brazo import BrazoEnv

if __name__ == '__main__':
    
    model_name = "Brazo_ppo_xyz_v2.zip"
    
    # Limpiamos el historial viejo
    if os.path.exists(model_name):
        os.remove(model_name)
        print("Modelo viejo borrado. Empezando en limpio.")

    # Ajustado a 6 núcleos para mantener temperaturas seguras y el PC estable
    n_nucleos = 6 
    print(f"Iniciando simulación en {n_nucleos} núcleos paralelos...")

    vec_env = make_vec_env(
        lambda: BrazoEnv(render=False), 
        n_envs=n_nucleos, 
        vec_env_cls=SubprocVecEnv
    )
    env = VecMonitor(vec_env)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Motor de IA en: {device}")

    model = PPO(
        "MlpPolicy", 
        env, 
        verbose=1, 
        device=device,
        learning_rate=0.0003,
        n_steps=2048, 
        batch_size=64,
        ent_coef=0.01 
    )

    # --- EL SEGURO DE VIDA ---
    # Guardará una copia del modelo cada 10,000 pasos por entorno 
    # (Como tienes 6 entornos, verás un guardado en consola cada 60,000 pasos totales)
    checkpoint_callback = CheckpointCallback(
        save_freq=10000, 
        save_path='./checkpoints/',
        name_prefix='brazo_respaldo'
    )

    print("Iniciando entrenamiento acelerado (300,000 timesteps)...")
    
    # Lanzamos el entrenamiento con 300k pasos y el autoguardado activado
    model.learn(total_timesteps=300000, callback=checkpoint_callback)

    # Guardado final oficial
    model.save("Brazo_ppo_xyz_v3")
    print("¡Entrenamiento Completado con éxito!")
    
    env.close()