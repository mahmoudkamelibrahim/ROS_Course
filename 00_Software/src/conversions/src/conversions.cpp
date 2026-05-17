#include <rclcpp/rclcpp.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2/LinearMath/Matrix3x3.h>

class EulerQuatTf2Demo : public rclcpp::Node
{
public:
  EulerQuatTf2Demo() : Node("euler_quat_tf2_demo")
  {
    // radians
    this->declare_parameter<double>("roll", 3.14159);   // X
    this->declare_parameter<double>("pitch", 0.4);       // Y
    this->declare_parameter<double>("yaw", -0.06);         // Z

    double roll  = this->get_parameter("roll").as_double();
    double pitch = this->get_parameter("pitch").as_double();
    double yaw   = this->get_parameter("yaw").as_double();

    tf2::Quaternion q;
    q.setRPY(roll, pitch, yaw);  // roll-pitch-yaw (radians)

    // Convert quaternion back to roll-pitch-yaw
    double r2, p2, y2;
    tf2::Matrix3x3(q).getRPY(r2, p2, y2);

    RCLCPP_INFO(this->get_logger(),
      "Input Euler(rad): roll=%.6f pitch=%.6f yaw=%.6f",
      roll, pitch, yaw);

    RCLCPP_INFO(this->get_logger(),
      "Quaternion [x,y,z,w] from tf2: [%.6f, %.6f, %.6f, %.6f]",
      q.x(), q.y(), q.z(), q.w());

    RCLCPP_INFO(this->get_logger(),
      "Back to Euler(rad) via tf2: roll=%.6f pitch=%.6f yaw=%.6f",
      r2, p2, y2);
  }
};

int main(int argc, char** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<EulerQuatTf2Demo>());
  rclcpp::shutdown();
  return 0;
}