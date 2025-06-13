import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import struct
import threading

class ArduinoBridge(Node):
    def __init__(self):
        super().__init__('arduino_bridge')
        self.ser = serial.Serial('/dev/ttyACM0', 115200)
        self.create_subscription(Twist, 'robot/cmd_vel', self.cmd_vel_callback, 10)

        # Start a background thread for reading the serial data from Arduino
        thread = threading.Thread(target=self.read_serial_loop)
        thread.daemon = True
        thread.start()

    def cmd_vel_callback(self, msg):
        vx = msg.linear.x
        vy = msg.linear.y
        omega = msg.angular.z
        # Pack the data into binary format (3 floats)
        data = struct.pack('fff', vx, vy, omega)
        self.ser.write(data)  # Send packed data to Arduino

        self.get_logger().info(f"Sent to Arduino: vx={vx}, vy={vy}, omega={omega}")

    def read_serial_loop(self):
        while rclpy.ok():
            try:
                # Read the binary data back from Arduino (2 floats for left and right speed)
                data = self.ser.read(8)
                if len(data) == 8:
                    left_speed, right_speed = struct.unpack('ff', data)
                    self.get_logger().info(f"From Arduino: Left Speed={left_speed}, Right Speed={right_speed}")
            except Exception as e:
                self.get_logger().error(f"Serial error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = ArduinoBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()