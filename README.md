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

### 1.  Gazebo Simulation and MoveIt RViz
```bash
ros2 launch custom gazebo.launch.py
```

## Next Steps

**Add Hardware Support**