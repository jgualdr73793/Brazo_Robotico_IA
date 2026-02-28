import pybullet as p
import pybullet_data
import time
import os

# Conectar con GUI
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# Cargar piso
p.loadURDF("plane.urdf")

# Ruta absoluta al URDF (para evitar problemas)
urdf_path = os.path.join(os.getcwd(), "urdf", "mi_brazo.urdf")
print("Intentando cargar URDF desde:", urdf_path)

try:
    # Cargar tu brazo fijo al suelo (useFixedBase=True para que no caiga todo)
    robot_id = p.loadURDF(urdf_path, [0, 0, 0], useFixedBase=True)
    print("¡Brazo cargado exitosamente! ID:", robot_id)
except Exception as e:
    print("Error al cargar URDF:", e)

# Gravedad (para ver si los links se doblan si no hay control)
p.setGravity(0, 0, -9.81)

print("\nSimulación corriendo. Mueve la cámara con mouse:")
print("- Clic izquierdo + arrastrar: rotar")
print("- Rueda mouse: zoom")
print("- Clic derecho + arrastrar: mover vista")
print("Cierra la ventana para salir.")

while p.isConnected():
    p.stepSimulation()
    time.sleep(1./240.)

if p.isConnected():
    p.disconnect()
else:
    print("Conexión ya cerrada por el usuario (ventana cerrada)")