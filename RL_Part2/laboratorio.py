import pybullet as p
import pybullet_data
import time

def main():
    # 1. Conexión visual
    p.connect(p.GUI)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    
    # 2. Configuración del mundo
    p.resetSimulation()
    p.setGravity(0, 0, -9.81)
    p.loadURDF("plane.urdf")
    
    # 3. Carga del robot (ajusta la ruta si es necesario)
    robot_id = p.loadURDF("../urdf/mi_brazo.urdf", [0, 0, 0], useFixedBase=True)
    
    num_joints = p.getNumJoints(robot_id)
    print(f"Robot cargado con {num_joints} articulaciones.")

    # 4. Crear los Sliders (Barras deslizantes)
    joint_ids = []
    for i in range(num_joints):
        info = p.getJointInfo(robot_id, i)
        joint_name = info[1].decode("utf-8")
        # Creamos un slider para cada motor de -3.14 a 3.14
        slider = p.addUserDebugParameter(joint_name, -3.14, 3.14, 0)
        joint_ids.append(slider)

    # Botón para activar/desactivar gravedad (para pruebas)
    gravedad_btn = p.addUserDebugParameter("Gravedad (1=Si, 0=No)", 0, 1, 1)

    print("\n--- INSTRUCCIONES ---")
    print("Mueve los sliders a la derecha para valores POSITIVOS.")
    print("Mueve los sliders a la izquierda para valores NEGATIVOS.")
    print("Mira el brazo y dime: ¿Hacia dónde sube el Link 1?")
    
    while True:
        # Leer valor de gravedad
        g_val = p.readUserDebugParameter(gravedad_btn)
        p.setGravity(0, 0, -9.81 if g_val > 0.5 else 0)

        # Leer sliders y mover motores
        for i in range(num_joints):
            target_pos = p.readUserDebugParameter(joint_ids[i])
            
            # Usamos mucha fuerza (500) para que no haya duda
            p.setJointMotorControl2(
                bodyIndex=robot_id,
                jointIndex=i,
                controlMode=p.POSITION_CONTROL,
                targetPosition=target_pos,
                force=500.0
            )

        p.stepSimulation()
        time.sleep(1./240.)

if __name__ == "__main__":
    main()