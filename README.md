# ROS2 SO Arm101

SO ARM101 based on ROS2



## Install Dependencies

### 1. Install ROS2
**Recommended: Ubuntu 24 (ROS2 Jazzy recommended)**
```bash
wget http://fishros.com/install -O fishros && . fishros
```

### 2. Install Dependencies

**ROS2 Jazzy recommended**
```bash
sudo apt-get install ros-${ROS_DISTRO}-ros-gz
sudo apt-get install ros-${ROS_DISTRO}-gz-ros2-control
sudo apt-get install ros-${ROS_DISTRO}-ros2-controllers
sudo apt-get install ros-${ROS_DISTRO}-moveit*
```

### 3. Environment Variable Setup
**Add SO-ARM101 Model Files**
```bash
export GZ_SIM_RESOURCE_PATH="/home/your_user_name/ros2_so_arm101/src"
source ~/.bashrc
```
**Build the project**
```bash
cd /home/your_user_name/ros2_so_arm101
colcon build
source install/setup.bash
```

## Run

### 1.  Mujoco Simulation and MoveIt RViz
```bash
ros2 launch robot_bringup robot_bringup.launch.py
```
Standalone ROS 2 Node Control
```bash
ros2 run real_control arm_controller  # sim2real
ros2 run real_control real2sim  # real2sim
ros2 run real_control bidirectional_teleoperation  # sim2real or real2sim
```

### 2. MuJoCo simulation To Real_robot
```bash
ros2 launch robot_bringup robot_bringup.launch.py sim2real:=true
```
### 3. MuJoCo simulation To Real_robot
```bash
ros2 launch robot_bringup robot_bringup.launch.py real2sim:=true
```

### 4. Press 'q' to switch between Sim2Real and Real2Sim
```bash
ros2 launch robot_bringup robot_bringup.launch.py BiTeleoperation:=true
```


## Thanks
[https://github.com/LitchiCheng/mujoco-learning](https://github.com/LitchiCheng/mujoco-learning)

[https://github.com/fishros/install](https://github.com/fishros/install)

## Next Steps

**RL Training**