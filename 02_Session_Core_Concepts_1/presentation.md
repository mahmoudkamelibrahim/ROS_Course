---
marp: true
theme: default
class: lead
paginate: true
backgroundColor: #fff
---

# Session 2: Messages & Topics
ROS 2 Jazzy C++ Course

---

## The Publish-Subscribe Pattern

- One-to-many, many-to-one, or many-to-many communication.
- **Publisher**: Sends data to a specific topic.
- **Subscriber**: Receives data from a specific topic.
- Topics are identified by name (e.g., `/cmd_vel` or `/scan`).

---

## Messages

- Data structures passed over topics.
- Examples: 
  - `std_msgs/msg/String` (basic string)
  - `geometry_msgs/msg/Twist` (velocities)
- Strongly typed. In C++, imported via headers (e.g. `#include "std_msgs/msg/string.hpp"`).

---

## Node CLI Commands

- `ros2 node list`: Output a list of available nodes.
- `ros2 node info <node_name>`: Output information about a node (publishers, subscribers, services, actions).

---

## Topic CLI Commands

- `ros2 topic list`: See all active topics.
- `ros2 topic info <topic_name>`: Get topic type and publisher/subscriber count.
- `ros2 topic echo <topic_name>`: Print data being published.
- `ros2 topic hz <topic_name>`: Measure publishing frequency.
- `ros2 topic bw <topic_name>`: Display bandwidth used by topic.
- `ros2 topic delay <topic_name>`: Display delay of topic from timestamp in header.
- `ros2 topic find <topic_type>`: Output a list of available topics of a given type.
- `ros2 topic pub <topic_name> <topic_type> '<args>'`: Publish data to a topic.
- `ros2 topic type <topic_name>`: Print a topic's type.

---

## Service CLI Commands

- `ros2 service list`: Output a list of available services.
- `ros2 service call <service_name> <service_type> '<args>'`: Call a service.
- `ros2 service find <service_type>`: Output a list of available services of a given type.
- `ros2 service type <service_name>`: Output a service's type.


---

## A Classic Example: Turtlesim

- **Turtlesim** is a lightweight 2D simulator perfect for learning ROS 2.
- It helps visualize nodes, topics, services, and actions interacting!
- **Terminal 1** (Start the simulator node):
  `ros2 run turtlesim turtlesim_node`
- **Terminal 2** (Start the teleoperation node):
  `ros2 run turtlesim turtle_teleop_key`
- Keep Terminal 2 focused and use your arrow keys to drive the turtle.

---

## GUI for ROS visualization (RQT)

- **rqt_graph**: Visualize the node graph.

---

## C++ Publisher Example

```cpp
publisher_ = this->create_publisher<std_msgs::msg::String>("topic", 10);
timer_ = this->create_wall_timer(
  500ms, std::bind(&MinimalPublisher::timer_callback, this));
```
- A timer triggers periodic publishing.
- The `10` is the QoS queue size.

---

## Next Steps

- Check out the `topic_examples` library.
- Build the publisher and subscriber.
- Verify they communicate using `ros2 topic echo` and `rqt_graph`.
