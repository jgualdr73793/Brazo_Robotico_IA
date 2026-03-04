import pybullet as p
import pybullet_data
import time
import os

print("=== Iniciando simulación con controles por parámetros ===")

# Conectar con GUI
p.connect(p.GUI)

# Rutas
p.setAdditionalSearchPath(pybullet_data.getDataPath())  # para plane.urdf

# Cargar piso
p.loadURDF("plane.urdf")

# Cargar tu brazo
urdf_path = os.path.join(os.getcwd(), "urdf", "mi_brazo.urdf")
print("Cargando URDF desde:", urdf_path)

robot_id = p.loadURDF(urdf_path, [0, 0, 0], useFixedBase=True)
print("Brazo cargado! ID:", robot_id)

# Gravedad
p.setGravity(0, 0, -9.81)

# === Controles por parámetros (sliders en la barra lateral derecha) ===

# 1. Base (giro horizontal 360°)
base_slider = p.addUserDebugParameter("Base Yaw (giro)", -3.14, 3.14, 0.0)

# 2. Hombro (arriba/abajo)
shoulder_slider = p.addUserDebugParameter("Hombro Pitch", -1.57, 1.57, 0.0)

# 3. Codo
elbow_slider = p.addUserDebugParameter("Codo Pitch", -2.0, 2.0, 0.0)

# 4. Muñeca pitch (arriba/abajo)
wrist_pitch_slider = p.addUserDebugParameter("Muñeca Pitch", -1.57, 1.57, 0.0)

# 5. Muñeca roll (giro de palma)
wrist_roll_slider = p.addUserDebugParameter("Muñeca Roll", -3.14, 3.14, 0.0)

print("\nControles listos:")
print("- Mueve los sliders en la barra lateral derecha")
print("- O usa flechas del teclado para ajustar el valor seleccionado")
print("Cierra la ventana para salir")

# Bucle principal
while p.isConnected():
    # Leer valores de sliders
    base_angle = p.readUserDebugParameter(base_slider)
    shoulder_angle = p.readUserDebugParameter(shoulder_slider)
    elbow_angle = p.readUserDebugParameter(elbow_slider)
    wrist_pitch_angle = p.readUserDebugParameter(wrist_pitch_slider)
    wrist_roll_angle = p.readUserDebugParameter(wrist_roll_slider)

    # Aplicar a los joints (índices 0,1,2,3,4 según el orden en tu URDF)
    p.setJointMotorControl2(robot_id, 0, p.POSITION_CONTROL, base_angle, force=300)
    p.setJointMotorControl2(robot_id, 1, p.POSITION_CONTROL, shoulder_angle, force=200)
    p.setJointMotorControl2(robot_id, 2, p.POSITION_CONTROL, elbow_angle, force=120)
    p.setJointMotorControl2(robot_id, 3, p.POSITION_CONTROL, wrist_pitch_angle, force=100)
    p.setJointMotorControl2(robot_id, 4, p.POSITION_CONTROL, wrist_roll_angle, force=80)

    p.stepSimulation()
    time.sleep(1./240.)

p.disconnect()
print("Simulación terminada")