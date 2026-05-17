# Static Transform Publisher Examples

This directory contains examples of publishing static transforms in ROS 2.

## Overview

Static transforms are fixed, non-changing coordinate frame relationships. They are ideal for:
- Sensor mounting positions (e.g., camera relative to robot base)
- Fixed geometric relationships that don't change during operation
- One-time calibration offsets
- Initialization of coordinate frame hierarchies

## Files

### `launch/static_transforms.launch.py`
A Python launch file that demonstrates publishing multiple static transforms using the `tf2_ros` static_transform_publisher executable.

**Included transforms:**
- `map → odom`: Global frame to odometry origin
- `odom → base_link`: Odometry to robot center
- `base_link → camera_link`: Camera mounting position (10cm forward, 30cm up)
- `base_link → lidar_link`: LiDAR mounting position (25cm up)
- `base_link → imu_link`: IMU sensor location (5cm back, 10cm up)

**Usage:**
```bash
ros2 launch transform_examples static_transforms.launch.py
```

### `config/static_transforms.yaml`
A YAML configuration file that defines static transforms in a data-driven format. This approach makes it easy to adjust sensor positions without modifying code.

## Key Concepts

### Arguments Breakdown

The `static_transform_publisher` executable accepts these arguments:

```
--x, --y, --z              Translation in meters
--roll, --pitch, --yaw     Rotation in radians
--frame-id                 Parent frame name
--child-frame-id           Child frame name
```

### Coordinate Frame Hierarchy

Static transforms form a tree structure. Each child frame has exactly one parent:

```
map (fixed global frame)
└── odom (odometry origin)
    └── base_link (robot center)
        ├── camera_link (front camera)
        ├── lidar_link (top sensor)
        ├── imu_link (IMU sensor)
        └── wheel_odom_link (wheel encoders)
```

### Example: Sensor Mounting

To mount a camera 10 cm forward and 30 cm above the robot's center:

```python
Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    arguments=[
        '--x', '0.1',      # 10 cm forward
        '--y', '0.0',      # centered
        '--z', '0.3',      # 30 cm up
        '--roll', '0.0',
        '--pitch', '0.0',
        '--yaw', '0.0',
        '--frame-id', 'base_link',
        '--child-frame-id', 'camera_link'
    ]
)
```

### Rotation Examples

Rotations are specified in radians using RPY (Roll-Pitch-Yaw):

- **Roll** (X-axis rotation): 0.785 rad ≈ 45° (tilt left/right)
- **Pitch** (Y-axis rotation): 1.571 rad ≈ 90° (tilt forward/backward)
- **Yaw** (Z-axis rotation): 3.142 rad ≈ 180° (turn left/right)

Example - Camera tilted down 45°:
```python
'--roll', '0.0',
'--pitch', '0.785',  # 45° down
'--yaw', '0.0',
```

## Debugging and Verification

### View the Transform Tree

Generate a visual diagram of all transforms:

```bash
ros2 run tf2_tools view_frames
```

This creates a `frames.pdf` showing the frame hierarchy and all transforms.

### Echo Specific Transforms

Print a specific transform between two frames:

```bash
ros2 run tf2_ros tf2_echo map base_link
```

Output shows continuous updates:
```
At time 1234.567
- Translation: [0.0, 0.0, 0.0]
- Rotation: in Quaternion [0.0, 0.0, 0.0, 1.0]
```

### Monitor Transform Health

Check publication rates and latency:

```bash
ros2 run tf2_ros tf2_monitor
```

## Common Issues

### Problem: "Frame [child_frame] does not exist"
**Solution:** Ensure the parent frame is published before the child frame.

### Problem: Circular transform dependencies
**Solution:** Check your frame hierarchy for cycles. Each frame should have exactly one parent (except the root).

### Problem: Transform not updating or visible
**Solution:** 
1. Verify the launch file is running: `ros2 topic list | grep tf`
2. Check for any error messages: `ros2 topic echo /tf_static`

## Advanced: Programmatic Publishing in C++

For more control, publish static transforms in C++:

```cpp
#include <tf2_ros/static_transform_broadcaster.h>
#include <geometry_msgs/msg/transform_stamped.hpp>

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("tf_publisher");
    
    auto tf_broadcaster = std::make_shared<tf2_ros::StaticTransformBroadcaster>(node);
    
    geometry_msgs::msg::TransformStamped t;
    t.header.frame_id = "base_link";
    t.child_frame_id = "camera_link";
    
    // Translation
    t.transform.translation.x = 0.1;
    t.transform.translation.y = 0.0;
    t.transform.translation.z = 0.3;
    
    // Rotation (quaternion)
    t.transform.rotation.x = 0.0;
    t.transform.rotation.y = 0.0;
    t.transform.rotation.z = 0.0;
    t.transform.rotation.w = 1.0;
    
    tf_broadcaster->sendTransform(t);
    
    rclcpp::spin(node);
    return 0;
}
```

## Further Reading

- [ROS 2 tf2 Documentation](https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Tf2/Tf2-Main.html)
- [REP-105: Coordinate Frame Conventions](https://www.ros.org/reps/rep-0105.html)
- [Transform Frame Documentation](https://docs.ros.org/en/jazzy/Concepts/Intermediate/About-Tf2.html)
