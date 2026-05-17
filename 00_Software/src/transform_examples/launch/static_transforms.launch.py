"""
Example Launch File: Static Transform Publisher

This launch file demonstrates how to publish static transforms in ROS 2.
Static transforms are fixed, non-changing coordinate frame relationships.

Example transforms published:
  - map -> odom: Maps the global map frame to odometry origin
  - odom -> base_link: Odometry frame to robot base
  - base_link -> camera_link: Robot base to camera sensor
  - base_link -> lidar_link: Robot base to lidar sensor

Author: ROS 2 Course
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """Generate launch description with static transform publishers."""
    
    return LaunchDescription([
        # Transform 1: map -> odom
        # This establishes the relationship between the global map frame
        # and the odometry frame (usually the starting position of the robot)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.0',      # Translation (meters)
                '--y', '0.0',
                '--z', '0.0',
                '--roll', '0.0',   # Rotation (radians)
                '--pitch', '0.0',
                '--yaw', '0.0',
                '--frame-id', 'map',
                '--child-frame-id', 'odom'
            ],
            name='map_to_odom_broadcaster'
        ),

        # Transform 2: odom -> base_link
        # Defines the relationship between odometry frame and robot base center.
        # In a real system, this would be published by the robot's odometry node
        # and would change over time. For this static example, we fix it.
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.0',
                '--y', '0.0',
                '--z', '0.0',
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '0.0',
                '--frame-id', 'odom',
                '--child-frame-id', 'base_link'
            ],
            name='odom_to_base_link_broadcaster'
        ),

        # Transform 3: base_link -> camera_link
        # Specifies where the camera is mounted relative to the robot base.
        # Example: Camera is mounted 10 cm forward and 30 cm above the base center
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.1',      # 10 cm forward (X)
                '--y', '0.0',      # Center (Y)
                '--z', '0.3',      # 30 cm up (Z)
                '--roll', '0.0',
                '--pitch', '0.0',  # Pointing straight ahead
                '--yaw', '0.0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'camera_link'
            ],
            name='base_link_to_camera_broadcaster'
        ),

        # Transform 4: base_link -> lidar_link
        # Specifies where the LiDAR is mounted.
        # Example: LiDAR is on top, center, 25 cm above base center
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '0.0',      # Center (X)
                '--y', '0.0',      # Center (Y)
                '--z', '0.25',     # 25 cm up (Z)
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '0.0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'lidar_link'
            ],
            name='base_link_to_lidar_broadcaster'
        ),

        # Transform 5: base_link -> imu_link
        # Specifies where the IMU sensor is located.
        # Example: IMU is mounted slightly offset from center
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '--x', '-0.05',    # 5 cm back (X)
                '--y', '0.0',      # Center (Y)
                '--z', '0.1',      # 10 cm up (Z)
                '--roll', '0.0',
                '--pitch', '0.0',
                '--yaw', '0.0',
                '--frame-id', 'base_link',
                '--child-frame-id', 'imu_link'
            ],
            name='base_link_to_imu_broadcaster'
        ),
    ])
