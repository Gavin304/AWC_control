import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus
import json
from std_msgs.msg import String

#!/usr/bin/env python3

class Nav2Commander(Node):
    def __init__(self):
        super().__init__('nav2_commander')
        self.pose_sub = self.create_subscription(
            PoseWithCovarianceStamped, 
            '/amcl_pose', 
            self.pose_callback, 
            10
        )
        self.command_sub = self.create_subscription(
            String,
            '/chatgpt_command',
            self.command_callback,
            10
        )
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.goal_handle = None

    def pose_callback(self, msg):
        self.get_logger().info(f'Received current pose: {msg.pose.pose}')

    def command_callback(self, msg):
        try:
            command_data = json.loads(msg.data)
            if command_data.get("command", {}).get("navigate") == "True":
                target_locations = command_data.get("target_locations", [])
                for location in target_locations:
                    pose = location.get("pose")
                    if pose:
                        self.send_goal(self.create_pose_stamped(pose))
        except json.JSONDecodeError as e:
            self.get_logger().error(f"Failed to decode command: {e}")

    def create_pose_stamped(self, pose):
        pose_stamped = PoseWithCovarianceStamped()
        pose_stamped.pose.pose.position.x = pose[0]
        pose_stamped.pose.pose.position.y = pose[1]
        pose_stamped.pose.pose.position.z = pose[2]
        pose_stamped.pose.pose.orientation.x = pose[3]
        pose_stamped.pose.pose.orientation.y = pose[4]
        pose_stamped.pose.pose.orientation.z = pose[5]
        pose_stamped.pose.pose.orientation.w = pose[6]
        return pose_stamped

    def send_goal(self, pose_stamped):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = pose_stamped
        self.action_client.wait_for_server()
        self.goal_handle = self.action_client.send_goal_async(
            goal_msg, 
            feedback_callback=self.feedback_callback
        )
        self.goal_handle.add_done_callback(self.goal_response_callback)

    def feedback_callback(self, feedback):
        if feedback:
            self.get_logger().info('Navigating...')

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self.get_logger().info('Goal accepted')

    def cancel_goal(self):
        if self.goal_handle:
            cancel_future = self.goal_handle.cancel_goal_async()
            cancel_future.add_done_callback(self.cancel_done_callback)

    def cancel_done_callback(self, future):
        if future.result().return_code == 0:
            self.get_logger().info('Goal successfully canceled')

def main(args=None):
    rclpy.init(args=args)
    node = Nav2Commander()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
