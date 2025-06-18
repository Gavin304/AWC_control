#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from rclpy.qos import QoSProfile
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from threading import Condition
from awc_interfaces.msg import NavigationCommand


class Nav2Commander(Node):
    def __init__(self):
        super().__init__('nav2_commander')
        qos = QoSProfile(depth=10)

        # Publisher for /current_pose
        self.pose_publisher_ = self.create_publisher(PoseStamped, '/current_pose', qos)
        self.get_logger().info('Publisher created for /current_pose')

        # Subscription to /amcl_pose topic
        self.amcl_subscription = self.create_subscription(
            PoseStamped, '/amcl_pose', self.amcl_pose_callback, qos
        )
        self.get_logger().info('Subscriber created for /amcl_pose')

        # Subscription to /navigate_command topic
        self.navigate_subscription = self.create_subscription(
            NavigationCommand, '/navigate_command', self.handle_navigation_command, qos
        )
        self.get_logger().info('Subscriber created for /navigate_command')

        # Create an action client for NavigateToPose
        self._navigate_action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # Timer to publish current_pose every second
        self.create_timer(1.0, self.publish_current_pose)
        self.get_logger().info('Current Pose Timer created')

        # Initialize current pose received from /amcl_pose
        self.current_pose = PoseStamped()

        # Track the state of goal
        self.goal_active = False

        # Condition to wait for goal completion
        self.goal_condition = Condition()

    def amcl_pose_callback(self, msg):
        """
        Callback for /amcl_pose subscription.
        Updates the current pose of the robot.
        """
        self.current_pose = msg

    def publish_current_pose(self):
        """
        Publishes the current pose to the /current_pose topic.
        """
        self.current_pose.header.stamp = self.get_clock().now().to_msg()
        self.pose_publisher_.publish(self.current_pose)

    def handle_navigation_command(self, msg):
        """
        Handles navigation commands received from the /navigate_command topic.
        :param msg: NavigationCommand message containing PoseStamped and navigate flag.
        """
        with self.goal_condition:
            if msg.navigate:  # Start navigation
                if not self.goal_active:
                    goal_msg = NavigateToPose.Goal()
                    goal_msg.pose = msg.pose  # Use the PoseStamped from the message

                    self.get_logger().info('Sending goal request...')
                    self._send_goal_future = self._navigate_action_client.send_goal_async(
                        goal_msg, feedback_callback=self.feedback_callback
                    )
                    self._send_goal_future.add_done_callback(self.goal_response_callback)

                    self.goal_active = True
            else:  # Stop navigation
                if self.goal_active:
                    self.get_logger().info('Stopping navigation...')
                    self._navigate_action_client.cancel_all_goals()
                    self.goal_active = False

    def goal_response_callback(self, future):
        """
        Callback for goal response.
        """
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            with self.goal_condition:
                self.goal_active = False
                self.goal_condition.notify_all()
            return

        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """
        Callback for goal result.
        """
        result = future.result().result
        self.get_logger().info(f'Goal status: {result}')
        with self.goal_condition:
            self.goal_active = False
            self.get_logger().info('Goal reached successfully')
            self.goal_condition.notify_all()

    def feedback_callback(self, feedback_msg):
        """
        Callback for feedback during goal execution.
        """
        # self.get_logger().info(f'Received feedback: {feedback_msg.feedback}')
        return


def main(args=None):
    rclpy.init(args=args)
    node = Nav2Commander()
    node.get_logger().info('Node initialized')

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        node.destroy_node()
        rclpy.shutdown()
        node.get_logger().info('Node shutdown')


if __name__ == '__main__':
    main()