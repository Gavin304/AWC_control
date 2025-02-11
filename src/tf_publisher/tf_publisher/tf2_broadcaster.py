import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
from math import sin, cos, pi
import numpy as np
import time

class AWCTFBroadcaster(Node):
    def __init__(self):
        super().__init__('tf2_broadcaster')
        self.br = TransformBroadcaster(self)
        self.timer = self.create_timer(0.1, self.handle_transform)

    def handle_transform(self):
        now = self.get_clock().now().to_msg()
        # Base transform
        base_t = TransformStamped()
        base_t.header.stamp = now
        base_t.header.frame_id = 'odom'
        base_t.child_frame_id = 'base_link'
        base_t.transform.translation.x = 0.0 # Change later
        base_t.transform.translation.y = 0.0 # Change later
        base_t.transform.translation.z = 0.0 # Change later
        theta = time.time() % (2.0 * pi)
        base_t.transform.rotation.z = sin(theta / 2)
        base_t.transform.rotation.w = cos(theta / 2)
        self.br.sendTransform(base_t)

        # Left wheel
        left_wheel_t = TransformStamped()
        left_wheel_t.header.stamp = now
        left_wheel_t.header.frame_id = 'base_link'
        left_wheel_t.child_frame_id = 'left_wheel'
        left_wheel_t.transform.translation.x = 0.3
        left_wheel_t.transform.translation.y = 0.2
        left_wheel_t.transform.translation.z = 0.0
        left_angle = time.time() % (2.0 * pi)
        left_wheel_t.transform.rotation.x = sin(left_angle / 2)
        left_wheel_t.transform.rotation.y = 0.0
        left_wheel_t.transform.rotation.z = 0.0
        left_wheel_t.transform.rotation.w = cos(left_angle / 2)
        self.br.sendTransform(left_wheel_t)

        # Right wheel
        right_wheel_t = TransformStamped()
        right_wheel_t.header.stamp = now
        right_wheel_t.header.frame_id = 'base_link'
        right_wheel_t.child_frame_id = 'right_wheel'
        right_wheel_t.transform.translation.x = 0.3
        right_wheel_t.transform.translation.y = -0.2
        right_wheel_t.transform.translation.z = 0.0
        right_angle = time.time() % (2.0 * pi)
        right_wheel_t.transform.rotation.x = sin(right_angle / 2)
        right_wheel_t.transform.rotation.y = 0.0
        right_wheel_t.transform.rotation.z = 0.0
        right_wheel_t.transform.rotation.w = cos(right_angle / 2)
        self.br.sendTransform(right_wheel_t)

def main(args=None):
    rclpy.init(args=args)
    node = AWCTFBroadcaster()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()