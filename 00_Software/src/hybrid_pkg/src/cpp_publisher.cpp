#include <chrono>
#include <functional>
#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int32.hpp"

using namespace std::chrono_literals;

class Int32Publisher : public rclcpp::Node {
public:
  Int32Publisher() : Node("int32_publisher"), count_(0) {
    // Create the publisher with topic name "int32_topic" and queue size 10
    publisher_ = this->create_publisher<std_msgs::msg::Int32>("int32_topic", 10);
    
    // Create a timer that executes the timer_callback every 1000ms (1 second)
    timer_ = this->create_wall_timer(
      1000ms, std::bind(&Int32Publisher::timer_callback, this));
  }

private:
  void timer_callback() {
    auto message = std_msgs::msg::Int32();
    message.data = count_++;
    RCLCPP_INFO(this->get_logger(), "Publishing Int32: %d", message.data);
    publisher_->publish(message);
  }

  rclcpp::TimerBase::SharedPtr timer_;
  rclcpp::Publisher<std_msgs::msg::Int32>::SharedPtr publisher_;
  int32_t count_;
};

int main(int argc, char * argv[]) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Int32Publisher>());
  rclcpp::shutdown();
  return 0;
}
