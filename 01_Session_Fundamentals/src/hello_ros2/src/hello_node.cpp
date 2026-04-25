#include "rclcpp/rclcpp.hpp"

class HelloNode : public rclcpp::Node {
public:
  HelloNode() : Node("hello_node") {
    // Print a hello world message through the ROS2 logger
    RCLCPP_INFO(this->get_logger(), "Hello, ROS 2 Jazzy! Welcome to Session 1.");
  }
};

int main(int argc, char ** argv) {
  // Initialize ROS 2
  rclcpp::init(argc, argv);
  
  // Create an instance of our node and spin it
  rclcpp::spin(std::make_shared<HelloNode>());
  
  // Shutdown ROS 2 gracefully
  rclcpp::shutdown();
  return 0;
}
