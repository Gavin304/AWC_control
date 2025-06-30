import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32, Int8
import serial
import struct
import threading
import math


class ArduinoBridge(Node):
    def __init__(self):
        super().__init__('arduino_bridge')

        # Parameters
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('wheel_radius', 0.08255)

        serial_port = self.get_parameter('serial_port').get_parameter_value().string_value
        self.WHEEL_RADIUS = self.get_parameter('wheel_radius').get_parameter_value().double_value

        self.ser = serial.Serial(serial_port, 115200, timeout=1)
        self.state = 0  # 0 = joystick, 1 = nav

        # Subscriptions
        self.create_subscription(Twist, '/cmd_vel_joy', self.cmd_vel_joy_callback, 10)
        self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_nav_callback, 10)
        self.create_subscription(Int8, 'state', self.state_callback, 10)

        # Publishers
        self.left_wheel_pub = self.create_publisher(Float32, 'awc_robot/left_wheel_velocity', 10)
        self.right_wheel_pub = self.create_publisher(Float32, 'awc_robot/right_wheel_velocity', 10)

        # Serial read thread
        thread = threading.Thread(target=self.read_serial_loop)
        thread.daemon = True
        thread.start()

    def state_callback(self, msg):
        self.state = msg.data

    def cmd_vel_joy_callback(self, msg):
        if self.state == 0:
            self.send_velocity(msg)

    def cmd_vel_nav_callback(self, msg):
        if self.state == 1:
            self.send_velocity(msg)

    def send_velocity(self, msg):
        vx = msg.linear.x
        vy = 0.0
        omega = msg.angular.z
        try:
            data = struct.pack('fff', vx, vy, omega)
            self.ser.write(data)
        except serial.SerialException as e:
            self.get_logger().error(f"Serial write error: {e}")

    def read_serial_loop(self):
        while rclpy.ok():
            try:
                data = self.ser.read(8)  # Expecting 2 floats (8 bytes)
                if len(data) == 8:
                    left_rpm, right_rpm = struct.unpack('ff', data)

                    left_rad_s = (left_rpm * 2 * math.pi) / 60.0
                    right_rad_s = (right_rpm * 2 * math.pi) / 60.0

                    self.get_logger().info(
                        f"Arduino RPM → L: {left_rpm:.2f}, R: {right_rpm:.2f} | rad/s → L: {left_rad_s:.2f}, R: {right_rad_s:.2f}"
                    )

                    self.left_wheel_pub.publish(Float32(data=left_rad_s))
                    self.right_wheel_pub.publish(Float32(data=right_rad_s))

            except Exception as e:
                self.get_logger().error(f"Serial read error: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = ArduinoBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
