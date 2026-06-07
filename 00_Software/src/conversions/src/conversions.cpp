#include <rclcpp/rclcpp.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2/LinearMath/Matrix3x3.h>
#include <vector>
#include <string>
#include <functional>

class ConversionsNode : public rclcpp::Node
{
public:
  ConversionsNode() : Node("conversions_cpp")
  {
    // Declare parameters with default values
    this->declare_parameter<double>("roll", 0.0);
    this->declare_parameter<double>("pitch", 0.0);
    this->declare_parameter<double>("yaw", 0.0);
    this->declare_parameter<double>("qx", 0.0);
    this->declare_parameter<double>("qy", 0.0);
    this->declare_parameter<double>("qz", 0.0);
    this->declare_parameter<double>("qw", 1.0);

    // Get current parameter values
    double roll  = this->get_parameter("roll").as_double();
    double pitch = this->get_parameter("pitch").as_double();
    double yaw   = this->get_parameter("yaw").as_double();
    double qx    = this->get_parameter("qx").as_double();
    double qy    = this->get_parameter("qy").as_double();
    double qz    = this->get_parameter("qz").as_double();
    double qw    = this->get_parameter("qw").as_double();

    // Register callback for dynamic parameter updates
    callback_handle_ = this->add_on_set_parameters_callback(
      std::bind(&ConversionsNode::parameters_callback, this, std::placeholders::_1));

    // Perform initial conversion
    perform_conversions(roll, pitch, yaw, qx, qy, qz, qw, false);
  }

private:
  void perform_conversions(double roll, double pitch, double yaw,
                           double qx, double qy, double qz, double qw,
                           bool updated)
  {
    std::string prefix = updated ? "[C++] Parameters updated! " : "[C++] ";

    // 1. RPY to Quaternion Conversion
    tf2::Quaternion q;
    q.setRPY(roll, pitch, yaw);

    RCLCPP_INFO(this->get_logger(), "%sRPY to Quaternion Conversion:", prefix.c_str());
    RCLCPP_INFO(this->get_logger(), "  Input RPY (rad): roll=%.6f, pitch=%.6f, yaw=%.6f",
                roll, pitch, yaw);
    RCLCPP_INFO(this->get_logger(), "  Output Quaternion [x, y, z, w]: [%.6f, %.6f, %.6f, %.6f]",
                q.x(), q.y(), q.z(), q.w());

    // 2. Quaternion to RPY Conversion
    tf2::Quaternion q_in(qx, qy, qz, qw);
    q_in.normalize(); // Normalize in case the input quaternion is not unit length

    double roll_out, pitch_out, yaw_out;
    tf2::Matrix3x3(q_in).getRPY(roll_out, pitch_out, yaw_out);

    RCLCPP_INFO(this->get_logger(), "%sQuaternion to RPY Conversion:", prefix.c_str());
    RCLCPP_INFO(this->get_logger(), "  Input Quaternion [x, y, z, w]: [%.6f, %.6f, %.6f, %.6f]",
                qx, qy, qz, qw);
    RCLCPP_INFO(this->get_logger(), "  Output RPY (rad): roll=%.6f, pitch=%.6f, yaw=%.6f",
                roll_out, pitch_out, yaw_out);
  }

  rcl_interfaces::msg::SetParametersResult parameters_callback(
    const std::vector<rclcpp::Parameter> & parameters)
  {
    rcl_interfaces::msg::SetParametersResult result;
    result.successful = true;
    result.reason = "success";

    double roll  = this->get_parameter("roll").as_double();
    double pitch = this->get_parameter("pitch").as_double();
    double yaw   = this->get_parameter("yaw").as_double();
    double qx    = this->get_parameter("qx").as_double();
    double qy    = this->get_parameter("qy").as_double();
    double qz    = this->get_parameter("qz").as_double();
    double qw    = this->get_parameter("qw").as_double();

    for (const auto & param : parameters) {
      if (param.get_name() == "roll") {
        roll = param.as_double();
      } else if (param.get_name() == "pitch") {
        pitch = param.as_double();
      } else if (param.get_name() == "yaw") {
        yaw = param.as_double();
      } else if (param.get_name() == "qx") {
        qx = param.as_double();
      } else if (param.get_name() == "qy") {
        qy = param.as_double();
      } else if (param.get_name() == "qz") {
        qz = param.as_double();
      } else if (param.get_name() == "qw") {
        qw = param.as_double();
      }
    }

    perform_conversions(roll, pitch, yaw, qx, qy, qz, qw, true);
    return result;
  }

  rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr callback_handle_;
};

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<ConversionsNode>());
  rclcpp::shutdown();
  return 0;
}