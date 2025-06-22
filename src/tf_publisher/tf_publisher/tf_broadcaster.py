#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.time import Time
from std_msgs.msg import Float64MultiArray, Float32
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import os
import yaml
import numpy as np
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped
import math
from ament_index_python.packages import get_package_share_directory
from tf_transformations import quaternion_from_euler


class AWCTFBroadcaster(Node):

    def __init__(self):
        super().__init__("awc_controller")

        # Declare parameters with default values
        self.declare_parameter('wheel_radius', 0.1651)
        self.declare_parameter('wheel_separation', 0.46)

        self.wheel_radius_ = self.get_parameter('wheel_radius').get_parameter_value().double_value
        self.wheel_separation_ = self.get_parameter('wheel_separation').get_parameter_value().double_value

        self.x_ = 0.0
        self.y_ = 0.0
        self.theta_ = 0.0

        self.wheel_cmd_pub_ = self.create_publisher(Float64MultiArray, "velocity_controller/commands", 10)
        # Change subscription to Twist
        self.vel_sub_ = self.create_subscription(Twist, "/cmd_vel_joy", self.velCallback, 10)
        self.odom_pub_ = self.create_publisher(Odometry, "/odom", 10)

        self.speed_conversion_ = np.array([[self.wheel_radius_/2, self.wheel_radius_/2],
                                           [self.wheel_radius_/self.wheel_separation_, -self.wheel_radius_/self.wheel_separation_]])

        # Fill the Odometry message with invariant parameters
        self.odom_msg_ = Odometry()
        self.odom_msg_.header.frame_id = "odom"
        self.odom_msg_.child_frame_id = "base_link"
        self.odom_msg_.pose.pose.orientation.x = 0.0
        self.odom_msg_.pose.pose.orientation.y = 0.0
        self.odom_msg_.pose.pose.orientation.z = 0.0
        self.odom_msg_.pose.pose.orientation.w = 1.0

        # Fill the TF message
        self.br_ = TransformBroadcaster(self)
        self.transform_stamped_ = TransformStamped()
        self.transform_stamped_.header.frame_id = "odom"
        self.transform_stamped_.child_frame_id = "base_link"

        self.last_v_ = 0.0
        self.last_w_ = 0.0

        self.timer_period_ = 0.02  # 50 Hz
        self.timer_ = self.create_timer(self.timer_period_, self.timerCallback)

        self.prev_time_ = self.get_clock().now()

        # timeout after which wheel data is considered stale (seconds)
        self.wheel_data_timeout_ = 0.5

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
        self.left_wheel_vel_ = msg.data
        self.last_wheel_time_ = self.get_clock().now()

    def right_wheel_cb(self, msg):
        self.right_wheel_vel_ = msg.data
        self.last_wheel_time_ = self.get_clock().now()

    def velCallback(self, msg):
        # Store last commanded velocities
        self.last_v_ = msg.linear.x
        self.last_w_ = msg.angular.z

        # Optionally publish wheel commands as before
        robot_speed = np.array([[self.last_v_], [self.last_w_]])
        wheel_speed = np.matmul(np.linalg.inv(self.speed_conversion_), robot_speed) 
        wheel_speed_msg = Float64MultiArray()
        # Swap the order here: [left, right]
        wheel_speed_msg.data = [wheel_speed[0, 0], wheel_speed[1, 0]]
        self.wheel_cmd_pub_.publish(wheel_speed_msg)

    def timerCallback(self):
        now = self.get_clock().now()
        dt = (now - self.prev_time_).nanoseconds / 1e9
        self.prev_time_ = now

        # if wheel data is stale, freeze velocities
        age = (now - self.last_wheel_time_).nanoseconds / 1e9
        if age > self.wheel_data_timeout_:
            left_vel = 0.0
            right_vel = 0.0
        else:
            left_vel = self.left_wheel_vel_
            right_vel = self.right_wheel_vel_

        # Integrate wheel angles
        self.left_wheel_angle_  += left_vel  * dt
        self.right_wheel_angle_ += right_vel * dt

        # --- here: use left_vel/right_vel, not the raw members ---
        v = self.wheel_radius_ * (right_vel + left_vel) / 2.0
        w = self.wheel_radius_ * (right_vel - left_vel) / self.wheel_separation_

        # Integrate to update pose
        self.theta_ += w * dt
        self.x_     += v * math.cos(self.theta_) * dt
        self.y_     += v * math.sin(self.theta_) * dt

        # Compose and publish the odom message
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

        # TF
        self.transform_stamped_.header.stamp = now.to_msg()
        self.transform_stamped_.header.frame_id = "odom"
        self.transform_stamped_.child_frame_id = "base_link"
        self.transform_stamped_.transform.translation.x = self.x_
        self.transform_stamped_.transform.translation.y = self.y_
        self.transform_stamped_.transform.translation.z = 0.0
        self.transform_stamped_.transform.rotation.x = q[0]
        self.transform_stamped_.transform.rotation.y = q[1]
        self.transform_stamped_.transform.rotation.z = q[2]
        self.transform_stamped_.transform.rotation.w = q[3]
        self.br_.sendTransform(self.transform_stamped_)

        # Wheel TFs (unchanged)
        wheel_y_offset = self.wheel_separation_ / 2.0

        left_wheel_tf = TransformStamped()
        left_wheel_tf.header.stamp = now.to_msg()
        left_wheel_tf.header.frame_id = "base_link"
        left_wheel_tf.child_frame_id = "left_wheel"
        left_wheel_tf.transform.translation.x = 0.0
        left_wheel_tf.transform.translation.y = wheel_y_offset
        left_wheel_tf.transform.translation.z = 0.0
        q_left = quaternion_from_euler(0, self.left_wheel_angle_, 0)
        left_wheel_tf.transform.rotation.x = q_left[0]
        left_wheel_tf.transform.rotation.y = q_left[1]
        left_wheel_tf.transform.rotation.z = q_left[2]
        left_wheel_tf.transform.rotation.w = q_left[3]
        self.br_.sendTransform(left_wheel_tf)

        right_wheel_tf = TransformStamped()
        right_wheel_tf.header.stamp = now.to_msg()
        right_wheel_tf.header.frame_id = "base_link"
        right_wheel_tf.child_frame_id = "right_wheel"
        right_wheel_tf.transform.translation.x = 0.0
        right_wheel_tf.transform.translation.y = -wheel_y_offset
        right_wheel_tf.transform.translation.z = 0.0
        q_right = quaternion_from_euler(0, self.right_wheel_angle_, 0)
        right_wheel_tf.transform.rotation.x = q_right[0]
        right_wheel_tf.transform.rotation.y = q_right[1]
        right_wheel_tf.transform.rotation.z = q_right[2]
        right_wheel_tf.transform.rotation.w = q_right[3]
        self.br_.sendTransform(right_wheel_tf)

        #self.get_logger().info(f"Publishing TF: x={self.x_}, y={self.y_}, theta={self.theta_}")


def main():
    rclpy.init()
    simple_controller = AWCTFBroadcaster()
    rclpy.spin(simple_controller)
    simple_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
