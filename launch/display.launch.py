import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import xacro

def generate_launch_description():

    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('my_bot'))
    xacro_file = os.path.join(pkg_path,'description','robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    
    # Create a robot_state_publisher node
    params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': use_sim_time}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )
    joint_state_publisher_params = {'use_gui': True}
    
    # Create the joint state publisher node
    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen',
        parameters=[joint_state_publisher_params]
    )
    rviz_params = {
        'config': LaunchConfiguration('rviz_config')  # Use LaunchConfiguration to specify the RViz config file
    }

    # Create the RViz node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[rviz_params]
    )

    # Declare a launch argument for the RViz config file path
    rviz_config_arg = DeclareLaunchArgument(
        'rviz_config',
        default_value='~/dev_ws/src/my_bot/config/view_bot.rviz',  # Set the default value to your RViz config file path
        description='Path to the RViz config file'
    )
    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),
        node_robot_state_publisher,
        joint_state_publisher_node,
        rviz_config_arg,
        rviz_node
    ])