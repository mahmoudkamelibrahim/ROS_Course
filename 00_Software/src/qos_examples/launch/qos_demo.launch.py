from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare launch arguments for the publisher's QoS settings
    pub_reliability_arg = DeclareLaunchArgument(
        'pub_reliability', default_value='reliable',
        description='QoS reliability for the C++ publisher (reliable or best_effort)'
    )
    pub_durability_arg = DeclareLaunchArgument(
        'pub_durability', default_value='volatile',
        description='QoS durability for the C++ publisher (volatile or transient_local)'
    )

    # Declare launch arguments for the subscriber's QoS settings
    sub_reliability_arg = DeclareLaunchArgument(
        'sub_reliability', default_value='reliable',
        description='QoS reliability for the Python subscriber (reliable or best_effort)'
    )
    sub_durability_arg = DeclareLaunchArgument(
        'sub_durability', default_value='volatile',
        description='QoS durability for the Python subscriber (volatile or transient_local)'
    )

    return LaunchDescription([
        pub_reliability_arg,
        pub_durability_arg,
        sub_reliability_arg,
        sub_durability_arg,

        # C++ Publisher Node
        Node(
            package='qos_examples',
            executable='qos_publisher',
            name='qos_publisher',
            parameters=[{
                'reliability': LaunchConfiguration('pub_reliability'),
                'durability': LaunchConfiguration('pub_durability'),
                'depth': 10,
                'publish_rate': 1.0
            }],
            output='screen'
        ),

        # Python Subscriber Node
        Node(
            package='qos_examples',
            executable='qos_subscriber.py',
            name='qos_subscriber',
            parameters=[{
                'reliability': LaunchConfiguration('sub_reliability'),
                'durability': LaunchConfiguration('sub_durability'),
                'depth': 10
            }],
            output='screen'
        )
    ])
