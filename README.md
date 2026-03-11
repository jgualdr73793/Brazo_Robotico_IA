# 🤖 Autonomous Robotic Arm Control: A Sim2Real RL Pipeline

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![PyBullet](https://img.shields.io/badge/Simulation-PyBullet-orange.svg)](https://pybullet.org/)
[![Reinforcement Learning](https://img.shields.io/badge/AI-Reinforcement%20Learning-success.svg)](#)
[![Status](https://img.shields.io/badge/Status-Active%20Development-brightgreen.svg)](#)

A Mechatronics Engineering and Artificial Intelligence research project focused on training an autonomous robotic arm using **Reinforcement Learning (RL)**. 

The ultimate goal of this repository is to build a robust **Sim2Real (Simulation to Reality) pipeline**. By training a Proximal Policy Optimization (PPO) agent within a physically accurate simulated environment (PyBullet), we establish the foundation to deploy zero-shot or fine-tuned AI policies directly onto physical hardware via ROS / ROS 2 and microcontrollers (ESP32).

---

## 🎥 Agent Demonstration (Simulated Environment)

> **Note:** The following demonstration showcases the RL agent making real-time control decisions to autonomously actuate its joints and stabilize at a target position.

<div align="center">
  <img src="![2026-03-11 12-11-31 - Trim](https://github.com/user-attachments/assets/b9794ece-f493-4573-bc4e-26c0406cf74e)
" alt="AI Robotic Arm Simulation" width="80%">
</div>

---

## 🧠 Project Architecture & Engineering Approach

This project bridges the gap between software-driven AI and physical mechatronic systems. The architecture is divided into three core phases:

1. **Kinematic Modeling & Simulation:** Importing a custom CAD design (`.stl` meshes) into PyBullet using a URDF framework to ensure accurate collision detection, inertia, and joint constraints.
2. **AI Training (Current Phase):** Developing a custom Gymnasium-based environment to train an RL agent (PPO). The reward function is optimized for trajectory smoothing, target reaching, and stabilization.
3. **Hardware Deployment (Roadmap):** Architecting the translation of simulated actions into PWM signals for physical servos through serial communication and edge computing.

## 📂 Repository Structure

* `urdf/`: Contains the physical and kinematic description of the robot.
  * `mesh/`: 3D structural models (`Link1.stl` to `Link4.stl` and base components).
  * `mi_brazo.urdf`: Main configuration file defining the robot's physical properties for PyBullet.
* `primera_sim.py` / `segunda_sim.py` / `3era_Sim.py`: Iterative physics testing scripts for tuning simulator dynamics.
* `entrenamiento.py`: Core script for initializing the virtual environment and training the RL agent.
* `Brazo_ppo.zip`: Stored weights and policy of the trained AI model.
* `Test.py`: Evaluation script to load the trained model and visually test its performance in the PyBullet environment.
* `requirements.txt`: Python environment dependencies.

## 🛠️ Tech Stack & Tools

* **Core Programming:** Python 3.12
* **Physics Simulation:** PyBullet
* **AI & Machine Learning:** Reinforcement Learning (PPO), Gymnasium Framework
* **CAD & Modeling:** SolidWorks / Blender (exported to `.stl` and `.urdf`)
* **Future Hardware Integration:** ROS / ROS 2, ESP32, Serial Communication

## ⚙️ Quick Start Guide

To replicate this simulation environment on your local machine:

1. **Clone the repository:**
   ```bash
   git clone [https://https://github.com/jgualdr73793/Brazo_Robotico_IA)
