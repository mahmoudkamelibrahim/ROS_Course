#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class Int32Subscriber(Node):
    def __init__(self):
        super().__init__('int32_subscriber')
        # Create a subscription to "int32_topic" with message type Int32 and queue depth of 10
        self.subscription = self.create_subscription(
            Int32,
            'int32_topic',
            self.listener_callback,
            10
        )
        self.subscription  # prevent unused variable warning
        self.get_logger().info('Int32 Subscriber Node started, listening on "int32_topic"...')

    def listener_callback(self, msg):
        self.get_logger().info(f'Received Int32: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = Int32Subscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
