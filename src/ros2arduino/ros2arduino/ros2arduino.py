import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial
import struct
import threading

class ArduinoBridge(Node):
    def __init__(self):
        super().__init__('arduino_bridge')
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        self.create_subscription(Twist, '/cmd_vel_joy', self.cmd_vel_callback, 10)

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
                    # Unpack the 8 bytes into two floats
                    left_speed, right_speed = struct.unpack('ff', data)
                    # =========================================================
                    # --- UNCOMMENTED THIS LINE TO SEE THE OUTPUT ---
                    self.get_logger().info(f"From Arduino -> Left RPM: {left_speed:.2f}, Right RPM: {right_speed:.2f}")
                    # =========================================================
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