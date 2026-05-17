**ROS2 Sensor Monitoring Station**

### Objective
Build a simple **Sensor Monitoring Station** that fuses data from a 2D LiDAR and ultrasonic sensor. The system allows real-time alert threshold adjustment using a potentiometer, demonstrates **Topics**, **Launch Files**, and **Parameters**, performs basic statistics on LaserScan data, and visualizes the result in RViz.

**Main Concepts**: Topics, Launch Files, Parameters, and hardware integration.

---

### Hardware Requirements & Setup

**Components:**
- PC with ROS2
- 2D LiDAR (RPLIDAR A1)
- Arduino Uno
- HC-SR04 Ultrasonic sensor
- 10kΩ Potentiometer

**Hardware Setup Tips:**
- Connect LiDAR to PC via USB. Check port (`ls /dev/ttyUSB*`) and run `sudo chmod 666 /dev/ttyUSB0`.
- **Arduino Wiring**:
  - HC-SR04: VCC → 5V, GND → GND, Trig → Pin 9, Echo → Pin 10
  - Potentiometer: Left → 5V, Right → GND, Middle → A0
- Mount both sensors facing the same direction at the same height on a stand.
- Face an open area (1–3 meters clear) for testing.
- Test sensors individually in Arduino IDE Serial Monitor first.

---

### Project Requirements

#### Nodes
You must create / use and use the following nodes:

1. **rplidar_node** (from `rplidar_ros` package)  
   - Publishes raw laser data on topic `/scan`

2. **arduino_bridge** (custom node – Python recommended)  
   - Reads data from Arduino via serial  
   - Publishes:
     - `/ultrasonic` (`sensor_msgs/Range`)
     - `/pot_threshold` (`std_msgs/Float32`)

3. **monitor_node** (custom node – main logic)  
   - Subscribes to `/scan`, `/ultrasonic`, and `/pot_threshold`
   - Performs statistics in the LaserScan callback
   - Uses parameter + potentiometer value for alert logic
   - Publishes:
     - `/min_distance` (`std_msgs/Float32`): Minimum of ultrasonic & laserscan
     - `/alert` (`std_msgs/Bool`): True if min_distance < pot_threshold


#### Parameters
- Declare parameter `alert_threshold` (default = 0.8 meters) in `monitor_node`.
- Support overriding via launch file argument.

#### Launch File
- Create `monitor_station.launch.py`
- Start all three nodes
- Allow changing threshold from terminal:  
  `ros2 launch my_sensor_station monitor_station.launch.py alert_threshold:=1.2`

#### RViz Visualization
- Fixed Frame = `laser`
- Add only:
  - **LaserScan** display → Topic: `/scan`
  - **Range** display → Topic: `/ultrasonic`
- Save configuration as `monitor.rviz`

---

### Hints & Tips

**Development Order (Recommended):**
1. Setup LiDAR and verify `/scan` in RViz
2. Arduino sketch
3. `arduino_bridge` node
4. `monitor_node` (subscribers, statistics, publishers, parameter)
5. Launch file
6. RViz configuration

**Monitor Node Tips:**
- Update `alert_threshold` from both the declared parameter and incoming `/pot_threshold` messages (for live potentiometer control).
- Use a timer to publish `/min_distance` and `/alert` regularly.

**Testing Tips:**
- Use `ros2 topic echo`, `ros2 topic list`, and `rqt_graph` frequently.
- Rotate the potentiometer and confirm alert behavior changes immediately.
- Move objects in front of the sensors and observe changes in RViz and topics.

**RViz Tips:**
- Set Fixed Frame to `laser`
- Adjust LaserScan size/color and Range color for clear visibility.