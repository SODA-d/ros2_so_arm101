from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    
    moveit_launch_path = get_package_share_directory('launch_moveit')

    moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(moveit_launch_path, 'launch', 'demo.launch.py')
        )
    )

    
    mujoco_viewer = Node(
        package='simulation_mujoco',
        executable='mujoco_viewer',
        name='mujoco_viewer',
        output='screen'
    )

    arm_controller = Node(
        package='real_control',
        executable='arm_controller',
        name='arm_controller',
        output='screen'
    )

   
    return LaunchDescription([
        moveit_launch,   
        mujoco_viewer, 
        # arm_controller      
    ])