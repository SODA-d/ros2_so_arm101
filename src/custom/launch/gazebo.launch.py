from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import TimerAction

def generate_launch_description():
    packagepath = get_package_share_directory('custom')


    moveit_config = (MoveItConfigsBuilder("so101",package_name="custom")
                    .robot_description('config/so101.gazebo.urdf.xacro')
                    .robot_description_semantic('config/so101.srdf')
                    .to_moveit_configs()
      )
    gazebo_node = IncludeLaunchDescription(
       PythonLaunchDescriptionSource([
            get_package_share_directory('ros_gz_sim')+'/launch/gz_sim.launch.py'],),
            launch_arguments=[('gz_args','empty.sdf -r')]
    )

    so101_to_gazebo_node = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-string',moveit_config.robot_description['robot_description'],'-x','0.0','-y','0.0','-z','0.0','-name','so101']
    )

    clock_bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'],
        output='screen'
    )

    robot_desc_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[moveit_config.robot_description,
                    {'use_sim_time':True},
                    {'publisher_frequency':30.0},]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='log',
        arguments=['-d',packagepath+'/config/moveit.rviz'],
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.planning_pipelines,
            moveit_config.joint_limits,
            {'use_sim_time':True}
        ]
    )

    ros2_control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            packagepath+'/config/ros2_controllers.yaml',
                    {'use_sim_time':True}],
        output='both'   
    )

    controller_spawner_node = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster','arm_controller','hand_controller',"--controller-manager", "/controller_manager"
        ]
    )

    move_group_node = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        output='screen',
        parameters=[moveit_config.to_dict(),
                    {'use_sim_time':True}]
    )


    
    return LaunchDescription([
        gazebo_node,
        robot_desc_node,
        clock_bridge_node,
        so101_to_gazebo_node,
        rviz_node,
        ros2_control_node,
        controller_spawner_node,
        move_group_node
    ])