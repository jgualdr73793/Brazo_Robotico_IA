import pybullet as p 
import pybullet_data
import time

# Conexiones y detalles Entorno
p.connect(p.GUI) # Conectar en modo GUI
p.setAdditionalSearchPath(pybullet_data.getDataPath()) # Configurar la ruta con datos de ejemplo
p.loadURDF("plane.urdf") # Se carga el piso
p.loadURDF("r2d2.urdf",[0, 0, 0.5]) # se carga el robot r2d2
p.setGravity(0, 0, -9.81) # se activa la gravedad

#Loop de simulación

while p.isConnected():
	p.stepSimulation()
	time.sleep(1./240.)

if p.isConnected():
	p.disconnect()
else:
	print("Conexión ya cerrada por el usuario (ventana cerrada)")
