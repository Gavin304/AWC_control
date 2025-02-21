#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from awc_msgs.srv import GetTransform
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
from tf2_ros import TransformBroadcaster, TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from geometry_msgs.msg import TransformStamped, Twist
from tf_transformations import quaternion_from_euler
import numpy as np

class AWCTFBroadcaster(Node):

    def __init__(self):
        super().__init__("awc_broadcaster")

        # TF Broadcaster
        self.static_tf_broadcaster_ = StaticTransformBroadcaster(self)
        self.dynamic_tf_broadcaster_ = TransformBroadcaster(self)

        # Static transform setup
        self.static_transform_stamped_ = TransformStamped()
        self.static_transform_stamped_.header.stamp = self.get_clock().now().to_msg()
        self.static_transform_stamped_.header.frame_id = "base_link"
        self.static_transform_stamped_.child_frame_id = "laser"
        self.static_transform_stamped_.transform.translation.x = 0.2
        self.static_transform_stamped_.transform.translation.y = 0.0
        self.static_transform_stamped_.transform.translation.z = 0.1
        self.static_transform_stamped_.transform.rotation.x = 0.0
        self.static_transform_stamped_.transform.rotation.y = 0.0
        self.static_transform_stamped_.transform.rotation.z = 0.0
        self.static_transform_stamped_.transform.rotation.w = 1.0

        self.static_tf_broadcaster_.sendTransform(self.static_transform_stamped_)
        self.get_logger().info("Publishing static transform between %s and %s" % 
                      (
                        self.static_transform_stamped_.header.frame_id,
                        self.static_transform_stamped_.child_frame_id
                      ))

        # Initialize variables
        self.prev_time = self.get_clock().now()
        self.last_x_ = 0.0
        self.last_y_ = 0.0
        self.last_theta_ = 0.0  # Orientation in radians
        self.linear_velocity_x_ = 0.0
        self.linear_velocity_y_ = 0.0
        self.angular_velocity_z_ = 0.0

        # Timer
        self.timer_ = self.create_timer(0.1, self.timerCallback)

        # Subscribe to cmd_vel topic
        self.cmd_vel_joy_subscription_ = self.create_subscription(
            Twist,
            "/cmd_vel_joy",
            self.cmdVel_joy_Callback,
            10
        )
        self.cmd_vel_joy_subscription_ = self.create_subscription(
            Twist,
            "/cmd_vel",
            self.cmdVelCallback,
            10
        )
        

        # Service Server
        self.get_transform_srv_ = self.create_service(GetTransform, "get_transform", self.getTransformCallback)
    def cmdVel_joy_Callback(self, msg: Twist):
        """Callback to update linear and angular velocities from cmd_vel & cmd_vel_joy."""
        self.linear_velocity_x_joy_ = msg.linear.x
        self.linear_velocity_y_joy_ = msg.linear.y
        self.angular_velocity_z_joy_ = msg.angular.z
    def cmdVelCallback(self, msg: Twist):
        """Callback to update linear and angular velocities from cmd_vel & cmd_vel_joy."""
        self.linear_velocity_x_command_ = msg.linear.x
        self.linear_velocity_y_command_ = msg.linear.y
        self.angular_velocity_z_command_ = msg.angular.z

    def timerCallback(self):
        """Timer callback to update the dynamic transformation."""
        current_time = self.get_clock().now()
        dt = (current_time - self.prev_time).nanoseconds / 1e9
        self.prev_time = current_time
        self.linear_velocity_x_ = self.linear_velocity_x_command_ + self.linear_velocity_x_joy_
        self.linear_velocity_y_ = 0.0 #Differential Drive
        self.angular_velocity_z_ = self.angular_velocity_z_command_ + self.angular_velocity_z_joy_

        # Update pose based on velocities
        self.last_theta_ += self.angular_velocity_z_ * dt
        self.last_theta_ = self.last_theta_ % (2 * np.pi)  # Keep theta in [0, 2π]
        self.last_x_ += (self.linear_velocity_x_ * np.cos(self.last_theta_) - self.linear_velocity_y_ * np.sin(self.last_theta_)) * dt
        self.last_y_ += (self.linear_velocity_x_ * np.sin(self.last_theta_) + self.linear_velocity_y_ * np.cos(self.last_theta_)) * dt

        # Convert updated orientation to quaternion
        q = quaternion_from_euler(0, 0, self.last_theta_)

        # Update and broadcast transform
        self.dynamic_transform_stamped_ = TransformStamped()
        self.dynamic_transform_stamped_.header.stamp = self.get_clock().now().to_msg()
        self.dynamic_transform_stamped_.header.frame_id = "odom"
        self.dynamic_transform_stamped_.child_frame_id = "base_link"
        self.dynamic_transform_stamped_.transform.translation.x = self.last_x_
        self.dynamic_transform_stamped_.transform.translation.y = self.last_y_
        self.dynamic_transform_stamped_.transform.translation.z = 0.0
        self.dynamic_transform_stamped_.transform.rotation.x = q[0]
        self.dynamic_transform_stamped_.transform.rotation.y = q[1]
        self.dynamic_transform_stamped_.transform.rotation.z = q[2]
        self.dynamic_transform_stamped_.transform.rotation.w = q[3]

        self.dynamic_tf_broadcaster_.sendTransform(self.dynamic_transform_stamped_)

    def getTransformCallback(self, req, res):
        """Service callback to get the requested transform."""
        self.get_logger().info("Requested Transform between %s and %s" % (req.frame_id, req.child_frame_id))
        try:
            requested_transform = self.tf_buffer_.lookup_transform(req.frame_id, req.child_frame_id, rclpy.time.Time())
            res.transform = requested_transform
            res.success = True
        except TransformException as e:
            self.get_logger().error("An error occurred while transforming %s and %s: %s" %
                                     (req.frame_id, req.child_frame_id, e))
            res.success = False
        return res

def main():
    rclpy.init()
    simple_tf_kinematics = AWCTFBroadcaster()
    rclpy.spin(simple_tf_kinematics)
    simple_tf_kinematics.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
