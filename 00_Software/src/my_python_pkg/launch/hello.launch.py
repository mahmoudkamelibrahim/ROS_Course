from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='my_python_pkg',
            executable='hello_node',
            name='hello_node',
            output='screen'
        )
    ])
