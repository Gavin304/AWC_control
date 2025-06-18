#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.constants import S_TO_NS
from rclpy.time import Time
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import JointState
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

        # EXTRACT DATA FROM PARAMETER CONFIG
        package_dir = get_package_share_directory('tf_publisher')
        yaml_file_path = os.path.join(package_dir, 'config', 'awc_description.yaml')
        with open(yaml_file_path, 'r') as file:
            config = yaml.safe_load(file)

        self.wheel_radius_ = config['wheel_radius']
        self.wheel_separation_ = config['wheel_separation']

        #Initialize Paramters
        self.wheel_radius_ = self.wheel_radius_ * 2
        self.wheel_separation_ = self.wheel_separation_ * 2

        self.x_ = 0.0
        self.y_ = 0.0
        self.theta_ = 0.0

        self.current_linear_ = 0.0
        self.current_angular_ = 0.0

        self.wheel_cmd_pub_ = self.create_publisher(Float64MultiArray, "velocity_controller/commands", 10)
        self.vel_sub_ = self.create_subscription(TwistStamped, "/cmd_vel_joy", self.velCallback, 10)
        self.odom_pub_ = self.create_publisher(Odometry, "awc_controller/odom", 10)

        self.br_ = TransformBroadcaster(self)
        self.transform_stamped_ = TransformStamped()
        self.transform_stamped_.header.frame_id = "odom"
        self.transform_stamped_.child_frame_id = "base_link"

        self.prev_time_ = self.get_clock().now()

        # Timer for fake odometry integration
        self.timer_ = self.create_timer(0.02, self.timerCallback)  # 50 Hz

        self.odom_msg_ = Odometry()

    def velCallback(self, msg):
        # Save the latest commanded velocities
        self.current_linear_ = msg.twist.linear.x
        self.current_angular_ = msg.twist.angular.z

        # Optionally publish wheel commands if needed
        robot_speed = np.array([[self.current_linear_],
                                [self.current_angular_]])
        wheel_speed = np.matmul(np.linalg.inv(self.speed_conversion_), robot_speed)
        wheel_speed_msg = Float64MultiArray()
        wheel_speed_msg.data = [wheel_speed[1, 0], wheel_speed[0, 0]]
        self.wheel_cmd_pub_.publish(wheel_speed_msg)

    def timerCallback(self):
        now = self.get_clock().now()
        dt = (now - self.prev_time_).nanoseconds / 1e9
        self.prev_time_ = now

        # Integrate pose using last commanded velocities
        d_theta = self.current_angular_ * dt
        self.theta_ += d_theta
        d_s = self.current_linear_ * dt
        self.x_ += d_s * math.cos(self.theta_)
        self.y_ += d_s * math.sin(self.theta_)

        # Compose and publish the odom message
        q = quaternion_from_euler(0, 0, self.theta_)
        self.odom_msg_.header.stamp = now.to_msg()
        self.odom_msg_.pose.pose.position.x = self.x_
        self.odom_msg_.pose.pose.position.y = self.y_
        self.odom_msg_.pose.pose.orientation.x = q[0]
        self.odom_msg_.pose.pose.orientation.y = q[1]
        self.odom_msg_.pose.pose.orientation.z = q[2]
        self.odom_msg_.pose.pose.orientation.w = q[3]
        self.odom_msg_.twist.twist.linear.x = self.current_linear_
        self.odom_msg_.twist.twist.angular.z = self.current_angular_
        self.odom_pub_.publish(self.odom_msg_)

        # TF
        self.transform_stamped_.transform.translation.x = self.x_
        self.transform_stamped_.transform.translation.y = self.y_
        self.transform_stamped_.transform.rotation.x = q[0]
        self.transform_stamped_.transform.rotation.y = q[1]
        self.transform_stamped_.transform.rotation.z = q[2]
        self.transform_stamped_.transform.rotation.w = q[3]
        self.transform_stamped_.header.stamp = now.to_msg()
        self.br_.sendTransform(self.transform_stamped_)


def main():
    rclpy.init()

    simple_controller = AWCTFBroadcaster()
    rclpy.spin(simple_controller)
    
    simple_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
