#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.time import Time
from std_msgs.msg import Float64MultiArray, Float32
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import numpy as np
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math
from tf_transformations import quaternion_from_euler


class AWCTFBroadcaster(Node):

    def __init__(self):
        super().__init__("awc_controller")

        self.declare_parameter('wheel_radius', 0.08255)
        self.declare_parameter('wheel_separation', 0.2325)

        self.wheel_radius_ = self.get_parameter('wheel_radius').get_parameter_value().double_value
        self.wheel_separation_ = self.get_parameter('wheel_separation').get_parameter_value().double_value

        self.x_ = 0.0
        self.y_ = 0.0
        self.theta_ = 0.0

        self.wheel_cmd_pub_ = self.create_publisher(Float64MultiArray, "velocity_controller/commands", 10)
        self.vel_sub_ = self.create_subscription(Twist, "/cmd_vel_joy", self.velCallback, 10)
        self.odom_pub_ = self.create_publisher(Odometry, "/odom", 10)

        self.speed_conversion_ = np.array([[self.wheel_radius_/2, self.wheel_radius_/2],
                                           [self.wheel_radius_/self.wheel_separation_, -self.wheel_radius_/self.wheel_separation_]])

        self.odom_msg_ = Odometry()
        self.odom_msg_.header.frame_id = "odom"
        self.odom_msg_.child_frame_id = "base_link"

        self.br_ = TransformBroadcaster(self)
        self.transform_stamped_ = TransformStamped()
        self.transform_stamped_.header.frame_id = "odom"
        self.transform_stamped_.child_frame_id = "base_link"

        self.last_v_ = 0.0
        self.last_w_ = 0.0

        self.timer_period_ = 0.02  # 50 Hz
        self.timer_ = self.create_timer(self.timer_period_, self.timerCallback)
        self.prev_time_ = self.get_clock().now()

        self.wheel_data_timeout_ = 0.2
        self.left_wheel_angle_ = 0.0
        self.right_wheel_angle_ = 0.0
        self.last_wheel_time_ = self.get_clock().now()
        self.left_wheel_vel_ = 0.0
        self.right_wheel_vel_ = 0.0

        self.left_wheel_sub_ = self.create_subscription(
            Float32, 'awc_robot/left_wheel_velocity', self.left_wheel_cb, 10)
        self.right_wheel_sub_ = self.create_subscription(
            Float32, 'awc_robot/right_wheel_velocity', self.right_wheel_cb, 10)

    def left_wheel_cb(self, msg):
        # msg.data is already in rad/s
        self.left_wheel_vel_ = msg.data
        self.last_wheel_time_ = self.get_clock().now()
        self.get_logger().info(f"[Left Wheel] rad/s: {self.left_wheel_vel_:.2f}")

    def right_wheel_cb(self, msg):
        self.right_wheel_vel_ = msg.data
        self.last_wheel_time_ = self.get_clock().now()
        self.get_logger().info(f"[Right Wheel] rad/s: {self.right_wheel_vel_:.2f}")

    def velCallback(self, msg):
        v = msg.linear.x
        w = msg.angular.z

        R = self.wheel_radius_
        L = self.wheel_separation_

        # differential-drive inverse kinematics:
        #   ω_left  = (2·v – w·L) / (2·R)
        #   ω_right = (2·v + w·L) / (2·R)
        wl = (2.0 * v - w * L) / (2.0 * R)
        wr = (2.0 * v + w * L) / (2.0 * R)

        msg_out = Float64MultiArray()
        msg_out.data = [wl, wr]
        self.wheel_cmd_pub_.publish(msg_out)

    def timerCallback(self):
        now = self.get_clock().now()
        dt = (now - self.prev_time_).nanoseconds / 1e9
        self.prev_time_ = now

        age = (now - self.last_wheel_time_).nanoseconds / 1e9
        if age > self.wheel_data_timeout_:
            left_vel = 0.0
            right_vel = 0.0
        else:
            left_vel = self.left_wheel_vel_
            right_vel = self.right_wheel_vel_

        self.left_wheel_angle_ += left_vel * dt
        self.right_wheel_angle_ += right_vel * dt

        v = self.wheel_radius_ * (right_vel + left_vel) / 2.0
        w = self.wheel_radius_ * (right_vel - left_vel) / self.wheel_separation_

        self.theta_ += w * dt
        self.x_ += v * math.cos(self.theta_) * dt
        self.y_ += v * math.sin(self.theta_) * dt

        q = quaternion_from_euler(0, 0, self.theta_)
        self.odom_msg_.header.stamp = now.to_msg()
        self.odom_msg_.pose.pose.position.x = self.x_
        self.odom_msg_.pose.pose.position.y = self.y_
        self.odom_msg_.pose.pose.orientation.x = q[0]
        self.odom_msg_.pose.pose.orientation.y = q[1]
        self.odom_msg_.pose.pose.orientation.z = q[2]
        self.odom_msg_.pose.pose.orientation.w = q[3]
        self.odom_msg_.twist.twist.linear.x = v
        self.odom_msg_.twist.twist.angular.z = w
        self.odom_pub_.publish(self.odom_msg_)

        # Log everything for diagnosis
        rpm_left = left_vel * 60 / (2 * math.pi)
        rpm_right = right_vel * 60 / (2 * math.pi)
        self.get_logger().info(
            f"Timer: dt={dt:.3f}s | RPM_L={rpm_left:.2f}, RPM_R={rpm_right:.2f} | v={v:.3f} m/s | x={self.x_:.3f} m"
        )

        self.transform_stamped_.header.stamp = now.to_msg()
        self.transform_stamped_.transform.translation.x = self.x_
        self.transform_stamped_.transform.translation.y = self.y_
        self.transform_stamped_.transform.translation.z = 0.0
        self.transform_stamped_.transform.rotation.x = q[0]
        self.transform_stamped_.transform.rotation.y = q[1]
        self.transform_stamped_.transform.rotation.z = q[2]
        self.transform_stamped_.transform.rotation.w = q[3]
        self.br_.sendTransform(self.transform_stamped_)

def main():
    rclpy.init()
    simple_controller = AWCTFBroadcaster()
    rclpy.spin(simple_controller)
    simple_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
