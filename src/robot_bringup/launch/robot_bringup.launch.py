from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription,DeclareLaunchArgument,OpaqueFunction,ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from ament_index_python.packages import get_package_share_directory

import os


def check_parameters(context):
    sim2real = LaunchConfiguration('sim2real').perform(context).lower() == 'true'
    real2sim = LaunchConfiguration('real2sim').perform(context).lower() == 'true'
    biteleoperation = LaunchConfiguration('BiTeleoperation').perform(context).lower() == 'true'
    
    true_params = []
    if sim2real:
        true_params.append('sim2real')
    if real2sim:
        true_params.append('real2sim')
    if biteleoperation:
        true_params.append('BiTeleoperation')
    
    if len(true_params) > 1:
        error_msg = f"""
        sim2real、real2sim 和 BiTeleoperation 
        这三个参数最多只能有一个为 true！
        """
        print(error_msg)
        raise RuntimeError("参数冲突：多个控制模式同时启用")
    
    return []

def generate_launch_description():

    sim2real = LaunchConfiguration('sim2real')
    declare_sim2real = DeclareLaunchArgument(
        'sim2real',
        default_value='false',
        description='Use simulation or real robot'
    )

    real2sim = LaunchConfiguration('real2sim')
    declare_real2sim = DeclareLaunchArgument(
        'real2sim',
        default_value='false',
        description='Use simulation or real robot'
    )

    BiTeleoperation = LaunchConfiguration('BiTeleoperation')
    declare_BiTeleoperation = DeclareLaunchArgument(
        'BiTeleoperation',
        default_value='false',
        description='Use simulation or real robot'
    )

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
        output='screen',
        condition=IfCondition(sim2real)
    )

    real2sim_controller = Node(
        package='real_control',
        executable='real2sim',
        name='real2sim',
        output='screen',
        condition=IfCondition(real2sim)
    )

    bidirectional_teleoperation = ExecuteProcess(
        cmd=['gnome-terminal', '--', 'ros2', 'run', 'real_control', 'bidirectional_teleoperation'],
        condition=IfCondition(BiTeleoperation),
        output='screen'
    )
   
    return LaunchDescription([
        declare_sim2real,
        declare_real2sim,
        declare_BiTeleoperation,
        OpaqueFunction(function=check_parameters),
        moveit_launch,   
        mujoco_viewer, 
        arm_controller,
        real2sim_controller,
        bidirectional_teleoperation    
    ])