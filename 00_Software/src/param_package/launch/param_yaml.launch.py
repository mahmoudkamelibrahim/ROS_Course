import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Locate the YAML file in the 'share' directory
    config = os.path.join(
        get_package_share_directory('param_package'),
        'config',
        'my_params.yaml'
    )

    return LaunchDescription([
        Node(
            package='param_package',
            executable='robot_speed',
            name='my_node',
            parameters=[config],  # 2. Pass the file path here
            output='screen'
        )
    ])
