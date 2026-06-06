# QoS Examples Package

This package demonstrates ROS 2 Quality of Service (QoS) policies, compatibility/matching contracts (Request vs. Offer), and incompatible QoS event callbacks in both C++ and Python.

## Package Structure

- `src/qos_publisher.cpp`: A C++ publisher node (`qos_publisher`) that publishes to `/qos_topic`. It takes ROS 2 parameters to configure its offered QoS profile and logs events using `incompatible_qos_callback` when a subscriber with incompatible QoS tries to connect.
- `scripts/qos_subscriber.py`: A Python subscriber node (`qos_subscriber`) that subscribes to `/qos_topic`. It also takes ROS 2 parameters to configure its requested QoS profile and logs incompatible QoS events.
- `launch/qos_demo.launch.py`: A launch file that starts both nodes and exposes their QoS configurations as launch arguments.

---

## Getting Started

### 1. Build the package

Make sure you are in the workspace root (`00_Software`):

```bash
cd ~/Documents/ROS2_Material/00_Software
colcon build --packages-select qos_examples
source install/setup.bash
```

### 2. Run Demos

#### Test Scenario A: Compatible QoS (Default)
Both the publisher and subscriber use standard `reliable` and `volatile` profiles.
```bash
ros2 launch qos_examples qos_demo.launch.py
```
*Observe that messages are published by the C++ node and successfully received by the Python node.*

#### Test Scenario B: Incompatible Reliability
The publisher offers a `best_effort` profile, while the subscriber requests a `reliable` profile.
```bash
ros2 launch qos_examples qos_demo.launch.py pub_reliability:=best_effort sub_reliability:=reliable
```
*Observe that no messages are received, and both nodes log warning messages pointing out the incompatible `RELIABILITY` policy.*

#### Test Scenario C: Incompatible Durability
The publisher offers a `volatile` profile, while the subscriber requests a `transient_local` profile.
```bash
ros2 launch qos_examples qos_demo.launch.py pub_durability:=volatile sub_durability:=transient_local
```
*Observe that no messages are received, and both nodes trigger callbacks logging that the mismatch is due to `DURABILITY`.*

---

## Checking QoS from the CLI

To debug QoS mismatch issues, you can run:

```bash
ros2 topic info /qos_topic --verbose
```

This will show details about the QoS profiles offered by every publisher and requested by every subscriber on that topic.
