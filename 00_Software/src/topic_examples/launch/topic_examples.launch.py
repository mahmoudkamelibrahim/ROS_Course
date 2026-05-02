from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Declare a configurable argument for the topic name
    topic_arg = DeclareLaunchArgument(
        'topic_name',
        default_value='topic',
        description='Topic name used by the publisher and subscriber')

    return LaunchDescription([
        topic_arg,

        Node(
            package='topic_examples',
            executable='publisher_node',
            name='minimal_publisher',
            remappings=[('topic', LaunchConfiguration('topic_name'))],
            output='screen',
        ),

        Node(
            package='topic_examples',
            executable='subscriber_node',
            name='minimal_subscriber',
            remappings=[('topic', LaunchConfiguration('topic_name'))],
            output='screen',
        ),
    ])
