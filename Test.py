import time
from stable_baselines3 import PPO
from Venv_Brazo import BrazoEnv

# 1. Cargar el modelo V1 (el traumado)
# Asegúrate de que el nombre sea el correcto (con o sin .zip)
model = PPO.load("Brazo_ppo_xyz_v1")

# 2. Crear entorno con render para ver la bola y el brazo
env = BrazoEnv(render=True) 

print("Iniciando visualización... Presiona Ctrl+C en la terminal para detener.")

while True: # Bucle infinito para ver muchos intentos
    obs, _ = env.reset()
    terminated = False
    truncated = False
    pasos = 0
    
    while not (terminated or truncated):
        # El modelo predice la acción
        action, _ = model.predict(obs, deterministic=True)
        
        # Aplicamos la acción
        obs, reward, terminated, truncated, info = env.step(action)
        
        # Un pequeño sleep para que tus ojos humanos sigan el movimiento
        time.sleep(0.01)
        pasos += 1
        
    print(f"Episodio terminado tras {pasos} pasos. Reintentando con nueva posición...")