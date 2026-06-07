import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Locate the YAML parameter file in share directory
    config = os.path.join(
        get_package_share_directory('conversions'),
        'config',
        'param.yaml'
    )

    return LaunchDescription([
        # C++ Conversions Node
        Node(
            package='conversions',
            executable='conversions_node',
            name='conversions_cpp',
            parameters=[config],
            output='screen'
        ),

        # Python Conversions Node
        Node(
            package='conversions',
            executable='conversions_node.py',
            name='conversions_python',
            parameters=[config],
            output='screen'
        )
    ])
