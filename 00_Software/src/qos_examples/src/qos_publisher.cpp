#include <chrono>
#include <functional>
#include <memory>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "rmw/types.h"

class QosPublisher : public rclcpp::Node
{
public:
  QosPublisher()
  : Node("qos_publisher")
  {
    // Declare parameters
    this->declare_parameter<std::string>("reliability", "reliable");
    this->declare_parameter<std::string>("durability", "volatile");
    this->declare_parameter<int>("depth", 10);
    this->declare_parameter<double>("publish_rate", 1.0);

    // Get parameters
    std::string reliability_str = this->get_parameter("reliability").as_string();
    std::string durability_str = this->get_parameter("durability").as_string();
    int depth = this->get_parameter("depth").as_int();
    double publish_rate = this->get_parameter("publish_rate").as_double();

    // Map strings to rclcpp QoS policies
    auto reliability = rclcpp::ReliabilityPolicy::Reliable;
    if (reliability_str == "best_effort") {
      reliability = rclcpp::ReliabilityPolicy::BestEffort;
    }

    auto durability = rclcpp::DurabilityPolicy::Volatile;
    if (durability_str == "transient_local") {
      durability = rclcpp::DurabilityPolicy::TransientLocal;
    }

    // Configure QoS Profile
    rclcpp::QoS qos(depth);
    qos.reliability(reliability);
    qos.durability(durability);

    // Set up incompatible QoS callback
    rclcpp::PublisherOptions pub_options;
    pub_options.event_callbacks.incompatible_qos_callback =
      [this](rclcpp::QOSOfferedIncompatibleQoSInfo & event) {
        RCLCPP_WARN(
          this->get_logger(),
          "\n=======================================================\n"
          "[qos_publisher] INCOMPATIBLE QOS OFFERED EVENT DETECTED!\n"
          "  Total incompatible subscriptions: %d (changed: +%d)\n"
          "  Last incompatible policy: %s\n"
          "=======================================================",
          event.total_count,
          event.total_count_change,
          policy_to_string(event.last_policy_kind).c_str()
        );
      };

    // Create the publisher
    publisher_ = this->create_publisher<std_msgs::msg::String>("qos_topic", qos, pub_options);

    // Create timer to publish messages
    auto interval = std::chrono::milliseconds(static_cast<int>(1000.0 / publish_rate));
    timer_ = this->create_wall_timer(
      interval, std::bind(&QosPublisher::publish_msg, this));

    RCLCPP_INFO(
      this->get_logger(),
      "Started QoS Publisher node on '/qos_topic':\n"
      "  - Reliability: %s\n"
      "  - Durability:  %s\n"
      "  - History:     Keep Last (Depth %d)\n"
      "  - Rate:        %.1f Hz",
      reliability_str.c_str(), durability_str.c_str(), depth, publish_rate
    );
  }

private:
  void publish_msg()
  {
    auto msg = std_msgs::msg::String();
    msg.data = "QoS message count: " + std::to_string(count_++);
    RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", msg.data.c_str());
    publisher_->publish(msg);
  }

  std::string policy_to_string(rmw_qos_policy_kind_t kind)
  {
    switch (kind) {
      case RMW_QOS_POLICY_DURABILITY:
        return "DURABILITY";
      case RMW_QOS_POLICY_DEADLINE:
        return "DEADLINE";
      case RMW_QOS_POLICY_LIVELINESS:
        return "LIVELINESS";
      case RMW_QOS_POLICY_RELIABILITY:
        return "RELIABILITY";
      case RMW_QOS_POLICY_HISTORY:
        return "HISTORY";
      case RMW_QOS_POLICY_LIFESPAN:
        return "LIFESPAN";
      default:
        return "UNKNOWN (" + std::to_string(kind) + ")";
    }
  }

  rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  int count_ = 0;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<QosPublisher>());
  rclcpp::shutdown();
  return 0;
}
