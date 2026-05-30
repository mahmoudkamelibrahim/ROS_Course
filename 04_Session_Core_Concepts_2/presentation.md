# Session 3:  Core Concepts 2
ROS 2 Jazzy C++ Course

---

## What We Cover Today

Beyond topics, ROS 2 provides richer communication and tooling patterns:

- **Services** — Request/response
- **Parameters** — Runtime node configuration
- **Launch Files** — Multi-node orchestration
- **Bags** — Recording and replaying data

---

## Services — Overview

- **Client-Server** pattern: one node *requests*, another *responds*.
- Used for operations that are **quick and discrete**:
  - Querying robot status
  - Triggering a calibration
  - Simple calculations (e.g., `AddTwoInts`)

---

## Services vs Topics

| Feature | Topic | Service |
|---|---|---|
| Pattern | Publish / Subscribe | Request / Response |
| Direction | One-to-many | One-to-one |
| Timing | Continuous / Async | On-demand |
| Use case | Sensor streams | Commands, queries |

---

## Service Definition (`.srv` file)

A `.srv` file defines the **Request** and **Response** separated by `---`:

```
# example_interfaces/srv/AddTwoInts.srv
int64 a
int64 b
---
int64 sum
```

- Fields above `---` → **Request**
- Fields below `---` → **Response**

---

## C++ Service Server

```cpp
#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

class AddTwoInts : public rclcpp::Node
{
public:
  AddTwoInts() : Node("add_two_ints")
  {
    service_ = this->create_service<example_interfaces::srv::AddTwoInts>(
        "add_two_ints", std::bind(&AddTwoInts::handle_add_two_ints, this, std::placeholders::_1, std::placeholders::_2));
  } 
private:
  void handle_add_two_ints(const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
                           std::shared_ptr<example_interfaces::srv::AddTwoInts::Response> response)
  {    response->sum = request->a + request->b;
    RCLCPP_INFO(this->get_logger(), "Incoming request\na: %ld b: %ld sum: %ld",
                request->a, request->b, response->sum);
  }
  rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr service_;
};


int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<AddTwoInts>();
  rclcpp::spin(node);
  rclcpp::shutdown();
}
```

---

```bash
# Example: call AddTwoInts directly
ros2 service call /add_two_ints \
  example_interfaces/srv/AddTwoInts "{a: 5, b: 6}"
```

---


## C++ Service Client

```cpp
#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

using namespace std::chrono_literals;

class AddTwoIntsClient : public rclcpp::Node
{
public:
  AddTwoIntsClient() : Node("add_two_ints_client")
  {
    client_ = this->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");
    send_request();
  }

private:
  void send_request()
  {
    auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
    request->a = 1;
    request->b = 2;
    while (!client_->wait_for_service(1s)) {
      RCLCPP_INFO(this->get_logger(), "Service not available, waiting again...");
    }
    auto result_future = client_->async_send_request(request);
    if (rclcpp::spin_until_future_complete(this->get_node_base_interface(), result_future) ==
        rclcpp::FutureReturnCode::SUCCESS)
    {
      RCLCPP_INFO(this->get_logger(), "Result of add_two_ints: %ld", result_future.get()->sum);
    } else {
      RCLCPP_ERROR(this->get_logger(), "Failed to call service add_two_ints");
    }
  }

  rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
};


int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<AddTwoIntsClient>();
  rclcpp::spin(node);
  rclcpp::shutdown();
}
```

```cpp
    if (!client_->wait_for_service(1s)) {
      RCLCPP_INFO(this->get_logger(), "Service not available");
      return;}

    // Send the request asynchronously
    auto result_future = client_->async_send_request(request, 
        [this](rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture future) {
            auto response = future.get();
            RCLCPP_INFO(this->get_logger(), "Result: %ld", response->sum);
        }
    );
```

---

## Service — CMakeLists.txt Changes

```cmake
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(example_interfaces REQUIRED)  # provides AddTwoInts.srv

add_executable(server src/add_two_ints_server.cpp)
ament_target_dependencies(server rclcpp example_interfaces)

add_executable(client src/add_two_ints_client.cpp)
ament_target_dependencies(client rclcpp example_interfaces)

install(TARGETS server client
  DESTINATION lib/${PROJECT_NAME})
```

---

## Service — package.xml Changes

```xml
<!-- Runtime + build dependency on the service interface package -->
<depend>rclcpp</depend>
<depend>example_interfaces</depend>
```

---

## Service CLI Commands

- `ros2 service list` — List all active services.
- `ros2 service type <service_name>` — Show the service type.
- `ros2 service find <service_type>` — Find services of a given type.
- `ros2 service call <name> <type> '<args>'` — Call a service from the terminal.



---

## Parameters — Overview

- **Parameters** are named configuration values declared inside a node.
- Supported types: `bool`, `int`, `double`, `string`, `arrays`.
- Can be set at launch time, from a YAML file, or changed at runtime via CLI.
- Nodes can **react to changes** at runtime using parameter callbacks.

---

## Declaring & Using Parameters (C++)

```cpp
#include <string>
#include "rclcpp/rclcpp.hpp"

class MyNode : public rclcpp::Node {
public:
  MyNode() : Node("my_node") {
    // 1. Declare parameters with default values
    this->declare_parameter<int>("speed", 10);
    this->declare_parameter<std::string>("robot_name", "carkyo");

    // 2. Read the values into local variables
    int speed = this->get_parameter("speed").as_int();
    std::string name = this->get_parameter("robot_name").as_string();

    // 3. Print the results
    RCLCPP_INFO(this->get_logger(), "Startup -> Robot: %s, Speed: %d", name.c_str(), speed);
  }
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  // Create the node and spin it
  auto node = std::make_shared<MyNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}

```

---

## Parameter CLI Commands

- `ros2 param list` — List all parameters on all running nodes.
- `ros2 param get <node> <param>` — Read a parameter value.
- `ros2 param set <node> <param> <value>` — Set a parameter at runtime.
- `ros2 param dump <node>` — Dump all parameters to a YAML file.
- `ros2 param load <node> <yaml_file>` — Load parameters from a YAML file.

```bash
# Set parameters at runtime
ros2 param set /my_node speed 25

# Run a node with initial parameter values
ros2 run param_package robot_speed --ros-args -p speed:=5 -p robot_name:="turtlebot"
```

---

## Parameter YAML File

Load parameters at launch using a YAML file:

```yaml
# config/my_params.yaml
my_node:
  ros__parameters:
    speed: 25
    robot_name: "carkyo"
```

**CMakeLists.txt** (C++):
```cmake
install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME}
)
```

**setup.py** (Python):
```python
(os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
```

**Run from terminal**:
```bash
ros2 run param_package robot_speed --ros-args --params-file src/param_package/config/my_params.yaml
ros2 run param_package robot_speed --ros-args --params-file $(ros2 pkg prefix param_package)/share/param_package/config/my_params.yaml
```

---

## Launch Files — Overview

- Written in **Python** (or XML / YAML, but Python is the standard).
- Start **multiple nodes** with a single command.
- Configure **namespaces**, **remappings**, **parameters**, and **arguments**.
- Essential for real systems with many packages working together.

---

## Minimal Launch File

```python
# launch/topic_examples.launch.py
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='topic_examples',
            executable='publisher_node',
            name='minimal_publisher',
            output='screen',
        ),
        Node(
            package='topic_examples',
            executable='subscriber_node',
            name='minimal_subscriber',
            output='screen',
        ),
    ])
```

---

## Launch File — CMakeLists.txt Changes

```cmake
find_package(ament_cmake REQUIRED)
find_package(launch_ros REQUIRED)   # only needed if you use launch Python API

# Install the launch directory so ros2 launch can find the file
install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch)
```

> The launch file itself is a plain Python script — no compilation needed.
> Just install the `launch/` folder so ROS 2 can locate it.

---

## Launch File — setup.py Changes

For **Python packages**, add the launch files to `data_files` in `setup.py`:

```python
import os
from glob import glob
# ...
setup(
    # ...
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Install launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        # Install config files (if any)
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
)
```

---

## Launch File — package.xml Changes

```xml
<!-- Needed to run the launch file -->
<exec_depend>launch</exec_depend>
<exec_depend>launch_ros</exec_depend>

<!-- Add exec_depend for every package whose nodes you launch -->
<exec_depend>topic_examples</exec_depend>
```

> `exec_depend` (not `depend`) because launch files are not compiled —
> they are only needed at runtime.

---

## Launch File Remapping

Change topic names at launch time without modifying code:

```python
# Remapping the topic name at launch time
Node(
    package='topic_examples',
    executable='publisher_node',
    name='minimal_publisher',
    remappings=[
        ('topic', 'chatter'),   # /topic → /chatter
    ],
    output='screen',
),
Node(
    package='topic_examples',
    executable='subscriber_node',
    name='minimal_subscriber',
    remappings=[
        ('topic', 'chatter'),   # must match publisher
    ],
    output='screen',
),
```

> **Note:** The `name` argument in the `Node` action overrides the node name 
> defined in your C++ code (e.g., `Node("my_node")`).

---

## Launch File Parameters

Pass parameters directly to a node inside the launch file:

```python
Node(
    package='param_package',
    executable='robot_speed',
    name='speedy_robot',
    parameters=[{
        'speed': 35,
        'robot_name': 'launch_bot'
    }],
    output='screen',
),
```

---

## Launch File — Parameters from YAML

The most common way to load parameters is from an external file:

```python
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
            parameters=[config],  # 2. Pass the file path here
            output='screen'
        )
    ])
```

---

## Launch CLI Commands

- `ros2 launch <pkg> <launch_file>` — Run a launch file.
- `ros2 launch <pkg> <launch_file> arg:=value` — Pass arguments.
- `ros2 launch <pkg> <launch_file> --show-args` — Show available arguments.

```bash
# Run with default topic name (/topic)
ros2 launch topic_examples topic_examples.launch.py

# Override the topic name at runtime
ros2 launch topic_examples topic_examples.launch.py topic_name:=chatter

# Show all available arguments without launching
ros2 launch topic_examples topic_examples.launch.py --show-args
```

---

## Bags — Overview

- `ros2 bag` records and replays topic data.
- Used for **debugging**, **testing**, and **offline development**.
- Replay a recording to re-run algorithms without real hardware.

---

## Recording a Bag

```bash
# Record all topics
ros2 bag record -a

# Record specific topics only
ros2 bag record /scan /cmd_vel /imu/data -o my_recording

# Record with a maximum size (in MB)
ros2 bag record -a --max-bag-size 500
```

The `-o` flag sets the output directory name.
Without it, a timestamped folder is created automatically.

---

## Inspecting a Bag

```bash
# Show metadata: topics, types, duration, message count
ros2 bag info my_recording/

# Example output:
# Topics:     /scan     [sensor_msgs/msg/LaserScan]   1200 msgs
#             /cmd_vel  [geometry_msgs/msg/Twist]       300 msgs
# Duration:   60s
```

---

## Replaying a Bag

```bash
# Replay all topics at original speed
ros2 bag play my_recording/

# Replay at 2x speed
ros2 bag play my_recording/ --rate 2.0

# Replay only specific topics
ros2 bag play my_recording/ --topics /scan /imu/data

# Loop playback indefinitely
ros2 bag play my_recording/ --loop
```

---

## Bag CLI Summary

| Command | Purpose |
|---|---|
| `ros2 bag record -a` | Record all topics |
| `ros2 bag record /topic` | Record specific topic(s) |
| `ros2 bag info <dir>` | Inspect bag contents |
| `ros2 bag play <dir>` | Replay a bag |
| `ros2 bag play --rate 2.0` | Replay at custom speed |
| `ros2 bag play --loop` | Loop playback |
| `ros2 bag play --topics /t` | Replay selected topics |
