# Lab 1: Core Concepts (Topics & Messages)

> **General Instructions:**
> *   **Dependencies:** Don't forget to add required dependencies (`rclcpp`, `rclpy`, `std_msgs`, `geometry_msgs`, `nav_msgs`, `sensor_msgs`) to your `package.xml`.
> *   **Build Configuration:** 
>     *   For **C++ tasks**, add `add_executable()` and `install(TARGETS ...)` entries to your `CMakeLists.txt`.
>     *   For **Python tasks**, add entry points to the `console_scripts` list in your `setup.py`.
> *   **Headers & Timestamps:**
>     *   **What is a Header?** A `header` (type `std_msgs/msg/Header`) is a standard field in many messages that provides metadata like `stamp` (time) and `frame_id` (coordinate frame).
>     *   **Timestamps:** Represent the exact moment data was captured, split into `sec` and `nanosec`. They are critical for synchronizing multiple sensors.
>     *   **Getting Current Time (C++):** `msg.header.stamp = this->get_clock()->now();`
>     *   **Getting Current Time (Python):** `msg.header.stamp = self.get_clock().now().to_msg()`
> *   **Complex Message Structures:**
>     *   Many messages have nested fields (e.g., `nav_msgs/msg/Odometry` has `pose.pose.position.x`).
>     *   **Feeding Data:** Access nested fields directly using dot notation (e.g., `msg.pose.pose.position.x = 1.0`, `msg->pose.pose.position.x = 1.0;`).
>     *   **Tip:** Use `ros2 interface show <message_type>` to see the exact structure and field names.


## Task 1: CPU Temperature Publisher
**Objective:** Build a ROS 2 C++ node to publish live CPU thermals.

**Specifications:**
- **Data Source:** Read `/sys/class/thermal/thermal_zone0/temp`.
- **Topic:** `/cpu_temp`
- **Rate:** 1 Hz.
- **Hint:** Use `<fstream>` to handle the file input.

**Example Output:**
```
data: 45.5
```

**Deliverables:**
- A functional node that logs and publishes real-time system data.
- Verified output via `ros2 topic echo /cpu_temp`.

## Task 2: Obstacle Detection Logic
**Objective:** Create a two-node Python system to simulate a distance sensor and a safety trigger.

**Specifications:**
- **Node A (Python):**
  - Simulate a sensor by publishing a random decimal between 0.03 and 5.0.
  - **Topic:** `/sensor/distance`
  - **Rate:** 10 Hz
  - **Hint:** Use `import random` and `random.uniform()`.
- **Node B (Python):**
  - Subscribe to `/sensor/distance`.
  - If the value is `< 2.0`, publish `True` to `/cmd/stop`.
  - Otherwise, publish `False`.

**Example Output:**
```
data: True (when distance is 1.45)
data: False (when distance is 2.5)
```

**Deliverables:**
- Both Python nodes running simultaneously.
- Verified logic using `ros2 topic echo /cmd/stop`.

## Task 3: Command Velocity Limiter
**Objective:** Create a C++ node to intercept, validate, and cap robot movement commands.

**Specifications:**
- **Input:** Subscribe to `/cmd_vel` (published by `teleop_twist_keyboard`).
- **Logic:**
  - Monitor linear speed and angular velocity.
  - If linear speed exceeds 1.0 m/s or angular velocity exceeds 1.5 rad/s, log a warning.
  - Change the values to these maximum limits.
- **Output:** Publish the capped values to `/cmd_vel_limited`.

**Hints:**
- Run teleop using: `ros2 run teleop_twist_keyboard teleop_twist_keyboard`
- Use `geometry_msgs/msg/Twist` for both input and output.

**Example Output:**
```
WARNING: Limiting linear speed to 1 m/s, Speed was: 1.06 m/s.
```

**Deliverables:**
- Functional node intercepting teleop commands.
- Verified output via `ros2 topic echo /cmd_vel_limited` while driving.



## Task 4: Odometry Path Publisher

**Objective:** Build a node (Python or C++) that simulates a moving robot by publishing synthetic Odometry data.

**Specifications:**
- **Logic:**
  - Maintain a variable for x position.
  - Increment x by 0.1 every cycle to simulate straight-line movement.
- **Output:** Publish to the /odom topic.
- **Rate:** 10 Hz.

**Hints:**
- **Message Type:** Use nav_msgs/msg/Odometry.
- **Orientation:** Set orientation.w = 1.0 (all other orientation values as 0.0).
- **Frames:** Set header.frame_id = "odom" and child_frame_id = "base_link".

**Example Output:**
```
header: 
    stamp: 
        sec: 1714420000
        nanosec: 44573999
    frame_id: "odom"
    child_frame_id: "base_link"
    pose: 
        pose:
          position: 
              x: 1.2
              y: 0.0
              z: 0.0
          orientation: 
              x: 0.0
              y: 0.0
              z: 0.0
              w: 1.0  
    twist:
        twist:
            linear: 
                x: 0.1
                y: 0.0
                z: 0.0 
            angular: 
                x: 0.0
                y: 0.0
                z: 0.0 
```

**Deliverables:**
- A functional node providing a time-stamped odometry stream.
- Verified output via `ros2 topic echo /odom`.




## Task 5: IMU CSV Playback Node

**Objective:** Build a Python node that reads IMU data from a CSV file and streams it as a live ROS 2 sensor feed.

**Specifications:**
- **Data Source:** Read from `imu_data.csv`. Loop back to the start after reaching the last row.
- **Output:** Publish to the `/imu/data` topic.
- **Rate:** 10 Hz.

**Hints:**
- **Message Type:** Use `sensor_msgs.msg.Imu`.
- **Absolute Path:** Use `os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'imu_data.csv'))` to find the CSV relative to the script.
- **CSV Parsing:** Use `import csv` and `csv.DictReader(file)` to load data into a list of dictionaries.
- **Timestamp:** Update `header.stamp` with the current time for every published message.

**Example Output:**
```
header: 
    stamp: 
        sec: 1714420000
        nanosec: 44573999
    frame_id: "base_link"
orientation: 
    x: 0.0
    y: 0.0
    z: 0.0
    w: 1.0
orientation_covariance: 
    [0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0]
angular_velocity: 
    x: 0.01
    y: -0.02
    z: 0.03
angular_velocity_covariance: 
    [0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0]
linear_acceleration: [x: 0.05, y: -0.12, z: 9.81]
linear_acceleration_covariance: 
    [0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0, 
    0.0, 0.0, 0.0]
```
