#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import math
from rcl_interfaces.msg import SetParametersResult

class ConversionsNode(Node):
    def __init__(self):
        super().__init__('conversions_python')
        
        # Declare parameters
        self.declare_parameter('roll', 0.0)
        self.declare_parameter('pitch', 0.0)
        self.declare_parameter('yaw', 0.0)
        self.declare_parameter('qx', 0.0)
        self.declare_parameter('qy', 0.0)
        self.declare_parameter('qz', 0.0)
        self.declare_parameter('qw', 1.0)
        
        # Get parameters
        roll = self.get_parameter('roll').value
        pitch = self.get_parameter('pitch').value
        yaw = self.get_parameter('yaw').value
        qx = self.get_parameter('qx').value
        qy = self.get_parameter('qy').value
        qz = self.get_parameter('qz').value
        qw = self.get_parameter('qw').value
        
        # Register callback for dynamic parameter updates
        self.add_on_set_parameters_callback(self.parameters_callback)
        
        # Perform initial conversion
        self.perform_conversions(roll, pitch, yaw, qx, qy, qz, qw, updated=False)

    def rpy_to_quaternion(self, roll, pitch, yaw):
        """
        Convert roll-pitch-yaw (in radians) to quaternion [x, y, z, w].
        Uses extrinsic XYZ / intrinsic ZYX sequence.
        """
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)

        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy

        return [x, y, z, w]

    def quaternion_to_rpy(self, x, y, z, w):
        """
        Convert quaternion [x, y, z, w] to roll-pitch-yaw (in radians).
        """
        # Normalize first
        norm = math.sqrt(x*x + y*y + z*z + w*w)
        if norm == 0.0:
            return [0.0, 0.0, 0.0]
        x /= norm
        y /= norm
        z /= norm
        w /= norm

        # Roll (x-axis rotation)
        sinr_cosp = 2.0 * (w * x + y * z)
        cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # Pitch (y-axis rotation)
        sinp = 2.0 * (w * y - z * x)
        if abs(sinp) >= 1.0:
            pitch = math.copysign(math.pi / 2.0, sinp)
        else:
            pitch = math.asin(sinp)

        # Yaw (z-axis rotation)
        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return [roll, pitch, yaw]

    def perform_conversions(self, roll, pitch, yaw, qx, qy, qz, qw, updated=False):
        prefix = "[Python] Parameters updated! " if updated else "[Python] "
        
        # 1. RPY to Quaternion
        qx_out, qy_out, qz_out, qw_out = self.rpy_to_quaternion(roll, pitch, yaw)
        
        self.get_logger().info(f"{prefix}RPY to Quaternion Conversion:")
        self.get_logger().info(f"  Input RPY (rad): roll={roll:.6f}, pitch={pitch:.6f}, yaw={yaw:.6f}")
        self.get_logger().info(f"  Output Quaternion [x, y, z, w]: [{qx_out:.6f}, {qy_out:.6f}, {qz_out:.6f}, {qw_out:.6f}]")

        # 2. Quaternion to RPY
        roll_out, pitch_out, yaw_out = self.quaternion_to_rpy(qx, qy, qz, qw)
        
        self.get_logger().info(f"{prefix}Quaternion to RPY Conversion:")
        self.get_logger().info(f"  Input Quaternion [x, y, z, w]: [{qx:.6f}, {qy:.6f}, {qz:.6f}, {qw:.6f}]")
        self.get_logger().info(f"  Output RPY (rad): roll={roll_out:.6f}, pitch={pitch_out:.6f}, yaw={yaw_out:.6f}")

    def parameters_callback(self, params):
        # Read current values
        roll = self.get_parameter('roll').value
        pitch = self.get_parameter('pitch').value
        yaw = self.get_parameter('yaw').value
        qx = self.get_parameter('qx').value
        qy = self.get_parameter('qy').value
        qz = self.get_parameter('qz').value
        qw = self.get_parameter('qw').value

        for param in params:
            if param.name == 'roll':
                roll = param.value
            elif param.name == 'pitch':
                pitch = param.value
            elif param.name == 'yaw':
                yaw = param.value
            elif param.name == 'qx':
                qx = param.value
            elif param.name == 'qy':
                qy = param.value
            elif param.name == 'qz':
                qz = param.value
            elif param.name == 'qw':
                qw = param.value

        self.perform_conversions(roll, pitch, yaw, qx, qy, qz, qw, updated=True)
        return SetParametersResult(successful=True, reason="success")

def main(args=None):
    rclpy.init(args=args)
    node = ConversionsNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
