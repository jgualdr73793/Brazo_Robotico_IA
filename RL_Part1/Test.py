import time
from stable_baselines3 import PPO
from Venv_Brazo import BrazoEnv

# Cargamos el entorno en modo visual
env = BrazoEnv(render=True)

# Cargamos tu modelo recién entrenado
print("Cargando cerebro del brazo...")
model = PPO.load("Brazo_ppo_xyz_v2")

obs, info = env.reset()

print("¡Iniciando prueba! Presiona Ctrl+C en la consola para detener.")
try:
    while True:
        # deterministic=True es la clave: apaga el "ruido" de entrenamiento
        # y hace que el brazo use su mejor movimiento posible.
        action, _states = model.predict(obs, deterministic=True)
        
        obs, reward, terminated, truncated, info = env.step(action)
        
        # Pausa ligera para que lo veamos a velocidad real y no en cámara rápida
        time.sleep(1./240.)
        
        if terminated or truncated:
            print("¡Objetivo alcanzado o tiempo agotado! Reiniciando...")
            time.sleep(1) # Pausa para celebrar antes de reiniciar
            obs, info = env.reset()
            
except KeyboardInterrupt:
    print("Prueba finalizada.")
    env.close()