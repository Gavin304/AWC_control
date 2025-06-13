import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int8, Bool

class WheelchairTeleop(Node):
    def __init__(self):
        super().__init__('wheelchair_teleop')
        self.vx = 0.0
        self.vy = 0.0
        self.w = 0.0
        self.state = Int8()
        self.state_count = 0

        self.create_subscription(Joy, 'joy', self.joy_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel_joy', 10)
        self.state_pub = self.create_publisher(Int8, 'state', 10)
        self.save_pose_pub = self.create_publisher(Bool, 'save_pose', 10)
        self.create_timer(0.02, self.timer_callback)

    def joy_callback(self, msg):
        # Map joystick axes to velocities
        self.vx = float(msg.axes[1])
        self.vy = 0.0
        self.w = float(msg.axes[3])

        # Toggle between joystick and navigation mode
        if msg.axes[6] == 1 or msg.axes[6] == -1:
            self.state_count += int(msg.axes[6])
            self.state.data = self.state_count % 2
            self.state_pub.publish(self.state)
            mode = 'Joystick' if self.state.data == 0 else 'Navigation'
            self.get_logger().info(f'State: {mode} mode')

        # Save pose (optional)
        if msg.buttons[8] == 1:
            self.save_pose_pub.publish(Bool(data=True))
            self.get_logger().info('Save Current Position.')

    def timer_callback(self):
        twist = Twist()
        twist.linear.x = self.vx
        twist.linear.y = 0.0
        twist.angular.z = self.w
        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = WheelchairTeleop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
