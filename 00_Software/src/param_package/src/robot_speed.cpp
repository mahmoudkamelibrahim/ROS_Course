#include "rclcpp/rclcpp.hpp"
#include <string> 

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
