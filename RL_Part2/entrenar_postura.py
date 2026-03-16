from stable_baselines3 import PPO
from RL_Part2.Venv_Postura import BrazoPosturaEnv # Aplicacion del __init__.py

def main():
    # Creamos el entorno de postura
    env = BrazoPosturaEnv(render=True)
    # Configuramos PPO usando MlpPolicy (solo usamos vectores simples, si fueran mas complejos o con mayor cantidad usamos Cnn)
    model = PPO("MlpPolicy", env, verbose=1, device = "cpu")

    print("Iniciamos el entrenamiento de la postura....")

    # 3. Entrenamos por 100,000 pasos (para postura es más que suficiente)
    model.learn(total_timesteps=100000)

    # 4. Guardamos el cerebro del robot
    model.save("brazo_postura_model")
    print("¡Modelo guardado en RL_Part2!")

if __name__ == '__main__':
    main()