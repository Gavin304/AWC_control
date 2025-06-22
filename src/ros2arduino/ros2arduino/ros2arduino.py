import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import struct
import threading
from std_msgs.msg import Float32

class ArduinoBridge(Node):
    def __init__(self):
        super().__init__('arduino_bridge')

        # Declare parameters with default values
        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.declare_parameter('wheel_radius', 0.1651)

        serial_port = self.get_parameter('serial_port').get_parameter_value().string_value
        self.WHEEL_RADIUS = self.get_parameter('wheel_radius').get_parameter_value().double_value

        self.ser = serial.Serial(serial_port, 115200, timeout=1)
        self.create_subscription(Twist, '/cmd_vel_joy', self.cmd_vel_callback, 10)

        # Publishers for wheel angular velocities (rad/s)
        self.left_wheel_pub = self.create_publisher(Float32, 'awc_robot/left_wheel_velocity', 10)
        self.right_wheel_pub = self.create_publisher(Float32, 'awc_robot/right_wheel_velocity', 10)

        # Start a background thread for reading the serial data from Arduino
        thread = threading.Thread(target=self.read_serial_loop)
        thread.daemon = True
        thread.start()
        self.get_logger().info("Arduino Bridge node started. Listening for commands...")

    def cmd_vel_callback(self, msg):
        vx = msg.linear.x
        vy = 0.0  # Always send 0 for vy, matching your Arduino code usage
        omega = msg.angular.z
        # Pack the data into binary format (3 floats)
        data = struct.pack('fff', vx, vy, omega)
        self.ser.write(data)  # Send packed data to Arduino

    def read_serial_loop(self):
        while rclpy.ok():
            try:
                # Wait for and read the binary data back from Arduino (2 floats = 8 bytes)
                data = self.ser.read(8)
                if len(data) == 8:
                    left_rpm, right_rpm = struct.unpack('ff', data)
                    # Convert RPM to rad/s
                    left_rad_s = (left_rpm / 60.0) * 2 * 3.14159265359
                    right_rad_s = (right_rpm / 60.0) * 2 * 3.14159265359

                    # Log raw and converted data
                    self.get_logger().info(
                        f"Arduino RPM    → left: {left_rpm:.2f} rpm, right: {right_rpm:.2f} rpm")
                    #self.get_logger().info(
                        #f"Arduino angular → left: {left_rad_s:.3f} rad/s, right: {right_rad_s:.3f} rad/s")

                    # Publish to topics
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