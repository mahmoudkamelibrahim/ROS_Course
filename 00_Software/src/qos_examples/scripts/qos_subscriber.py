#!/usr/bin/env python3

import sys
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy, QoSPolicyKind
from rclpy.event_handler import SubscriptionEventCallbacks
from std_msgs.msg import String

class QosSubscriber(Node):
    def __init__(self):
        super().__init__('qos_subscriber')

        # Declare parameters
        self.declare_parameter('reliability', 'reliable')
        self.declare_parameter('durability', 'volatile')
        self.declare_parameter('depth', 10)

        # Get parameters
        reliability_str = self.get_parameter('reliability').get_parameter_value().string_value
        durability_str = self.get_parameter('durability').get_parameter_value().string_value
        depth = self.get_parameter('depth').get_parameter_value().integer_value

        # Map strings to rclpy QoS policies
        reliability = ReliabilityPolicy.RELIABLE
        if reliability_str == 'best_effort':
            reliability = ReliabilityPolicy.BEST_EFFORT

        durability = DurabilityPolicy.VOLATILE
        if durability_str == 'transient_local':
            durability = DurabilityPolicy.TRANSIENT_LOCAL

        # Configure QoS Profile
        qos_profile = QoSProfile(
            history=HistoryPolicy.KEEP_LAST,
            depth=depth,
            reliability=reliability,
            durability=durability
        )

        # Define incompatible QoS callback
        def incompatible_qos_callback(event):
            try:
                # Convert the policy kind integer/enum to human readable name
                policy_name = QoSPolicyKind(event.last_policy_kind).name
            except Exception:
                policy_name = f"UNKNOWN ({event.last_policy_kind})"

            self.get_logger().warn(
                "\n=======================================================\n"
                "[qos_subscriber] INCOMPATIBLE QOS REQUESTED EVENT DETECTED!\n"
                f"  Total incompatible publishers: {event.total_count} (changed: +{event.total_count_change})\n"
                f"  Last incompatible policy: {policy_name}\n"
                "======================================================="
            )

        # Setup event callbacks
        event_callbacks = SubscriptionEventCallbacks(
            incompatible_qos=incompatible_qos_callback
        )

        # Create subscription
        self.subscription = self.create_subscription(
            String,
            'qos_topic',
            self.listener_callback,
            qos_profile=qos_profile,
            event_callbacks=event_callbacks
        )

        self.get_logger().info(
            "Started QoS Subscriber node on '/qos_topic':\n"
            f"  - Reliability: {reliability_str}\n"
            f"  - Durability:  {durability_str}\n"
            f"  - History:     Keep Last (Depth {depth})"
        )

    def listener_callback(self, msg):
        self.get_logger().info(f"Received message: '{msg.data}'")

def main(args=None):
    rclpy.init(args=args)
    node = QosSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
