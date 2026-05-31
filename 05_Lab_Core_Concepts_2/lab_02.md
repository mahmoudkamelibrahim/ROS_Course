# Lab 2: Core Concepts 2 (Custom Interfaces, Services, Parameters & Bags)

> **General Instructions:**
> *   **Dependencies:** Don't forget to add required dependencies (`rclcpp`, `std_msgs`, `geometry_msgs`, `turtlesim`, `std_srvs`) to your `package.xml`.
> *   **Build Configuration:** 
>     *   For **C++ tasks**, add `add_executable()` and `install(TARGETS ...)` entries to your `CMakeLists.txt`.
>     *   For **Custom Interfaces**, use `rosidl_generate_interfaces` in your `CMakeLists.txt`.
> *   **Tutorial:** For help with custom messages, refer to the [Official ROS 2 Jazzy Tutorial](https://docs.ros.org/en/jazzy/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html).

```
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotStatus.msg"
  DEPENDENCIES geometry_msgs std_msgs
)
------
rosidl_get_typesupport_target(cpp_typesupport_target
  ${PROJECT_NAME} rosidl_typesupport_cpp)

target_link_libraries(status_publisher "${cpp_typesupport_target}")

```

---

## Task: Circular Moving Turtle with Stop & Continue Services

### **Objective**
Create a ROS 2 package where a turtle moves continuously in a **circle** at a constant speed. The movement can be stopped and resumed using two simple services. A custom message is used to report the robot’s status.


---

### **Requirements**

#### **1. Custom Message (`msg/RobotStatus.msg`)**
```msg
geometry_msgs/Pose2D pose
string state           # "running" or "stopped"
float32 temperature
int32 lap_count
```

**Explanation of Message Fields:**
- `pose`: Current position and orientation of the turtle (x, y, theta).
- `state`: Current movement state ("running" or "stopped").
- `temperature`: Dummy temperature value (e.g., calculated based on movement).
- `lap_count`: Number of full circles (360 degrees) the turtle has completed.

---

#### **2. Parameters** (`params/patrol_params.yaml`)

```yaml
patrol_controller:
  ros__parameters:
    linear_speed: 1.5
    angular_speed: 1.0

status_publisher:
  ros__parameters:
    status_rate: 5.0
```

---

#### **3. Nodes**

| Node                | Main Responsibilities |
|---------------------|-----------------------|
| `status_publisher`  | Publishes `/robot/status` (custom message) at the rate defined in parameters. |
| `patrol_controller` | Makes turtle move in circle using the linear and angular speeds defined in parameters + provides `/stop` and `/continue` services. |

---

#### **4. Launch (`launch/patrol_robot.launch.py`)**
The launch file should start **3 nodes**:
1. `turtlesim_node`: From the `turtlesim` package.
2. `status_publisher`: One of the nodes you implemented.
3. `patrol_controller`: The other node you implemented, which should also load the parameters from `patrol_params.yaml`.

---

#### **5. Topics**

- `/robot/status` → Custom `RobotStatus` message (published by `status_publisher`).
- `/turtle1/cmd_vel` → `geometry_msgs/Twist` (published by `patrol_controller`).
- `/turtle1/pose` → `turtlesim/msg/Pose` (subscribed by `status_publisher` to fill status data).

---

#### **6. Services**

- `/stop` → `std_srvs/srv/Empty` → Stops the turtle movement.
- `/continue` → `std_srvs/srv/Empty` → Resumes circular movement.

---

### **Expected Behavior / Output**

1. After launching, the `turtlesim_node` opens and the turtle starts moving in a **smooth circle** immediately.
2. The `/robot/status` topic continuously publishes the robot’s current pose, state, temperature, and lap count.
3. When you call the `/stop` service, the turtle **stops moving** and the `state` in the custom message becomes `"stopped"`.
4. When you call the `/continue` service, the turtle **resumes** moving in a circle and the `state` becomes `"running"`.

---

### **Task: Bag Recording**
Record the following topics for **1-2 minutes** to capture movement, stopped states, and a change in rotation radius:
- `/robot/status`
- `/turtle1/cmd_vel`
- `/turtle1/pose`

```bash
ros2 bag record /robot/status /turtle1/cmd_vel /turtle1/pose -o turtle_patrol_bag

# After recording, verify the contents
ros2 bag info turtle_patrol_bag
```

---

### **How to Test**

```bash
# 1. Build and Source
colcon build --symlink-install --packages-select simple_turtle_patrol
source install/setup.bash

# 2. Run the system
ros2 launch simple_turtle_patrol patrol_robot.launch.py

# 3. In another terminal - Check status
ros2 topic echo /robot/status

# 4. Stop the turtle
ros2 service call /stop std_srvs/srv/Empty

# 5. Resume movement
ros2 service call /continue std_srvs/srv/Empty

# 6. Change parameters in YAML file (No Rebuild Needed)
# Edit 'params/patrol_params.yaml', then restart the launch.
# Because of --symlink-install, changes are reflected immediately.

# 7. Change parameters at runtime
ros2 param set /patrol_controller linear_speed 2.0
ros2 param set /patrol_controller angular_speed 1.0

```

---

### **Expected Package Structure**

```
simple_turtle_patrol/
├── msg/
│   └── RobotStatus.msg
├── params/
│   └── patrol_params.yaml
├── launch/
│   └── patrol_robot.launch.py
├── src/
│   ├── status_publisher.cpp
│   └── patrol_controller.cpp
├── CMakeLists.txt
├── package.xml
```

---

### **Deliverables**

1.  **The Package:** A functional `simple_turtle_patrol` package.
2.  **Visual Output:** 2 screenshots of `turtlesim` showing the circular path with 2 different diameters.
3.  **Data Log:** A 1-2 minute bag file (`turtle_patrol_bag`) containing data of the turtle moving, then being stopped, then continuing, and finally changing the rotation radius.
4.  **Bag Metadata:** A screenshot of the terminal showing the output of `ros2 bag info turtle_patrol_bag`.
