from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='param_package',
            executable='robot_speed',
            name='speedy_robot',
            parameters=[{
                'speed': 35,
                'robot_name': 'launch_bot'
            }],
            output='screen',
        ),
    ])
