import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from .Board import Board

class MasterPiDriveNode(Node):
    def __init__(self):
        super().__init__('masterpi_drive_node')
        
        # initialize connection to MasterPi chassis controller
        try:
            self.board = Board(device="/dev/ttyAMA0")
            self.get_logger().info("Successfully connected to MasterPi chassis controller (/dev/ttyAMA0)")
        except Exception as e:
            self.get_logger().error(f"Failed to open serial port: {e}")

        # subscribe to /cmd_vel topic
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10)
        
        # set a speed limit for motor commands (you can adjust this based on your hardware capabilities)
        self.speed_limit = 100 

    def cmd_vel_callback(self, msg):
        # Extract linear and angular velocity commands from the Twist message
        x = msg.linear.x   # Forward/backward
        y = msg.linear.y   # Left/right strafing
        z = msg.angular.z  # Rotation around vertical axis

        # Mecanum Kinematics
        # ID 1: LF, ID 2: LB, ID 3: RF, ID 4: RB
        pulse1 = (x - y - z) * self.speed_limit
        pulse2 = (x + y - z) * self.speed_limit
        pulse3 = (x + y + z) * self.speed_limit
        pulse4 = (x - y + z) * self.speed_limit

        # Limit values to -100 ~ 100
        speeds = [pulse1, pulse2, pulse3, pulse4]
        constrained_speeds = [[i + 1, max(min(s, 100), -100)] for i, s in enumerate(speeds)]

        # Execute motor commands
        self.board.set_motor_duty(constrained_speeds)

def main(args=None):
    rclpy.init(args=args)
    node = MasterPiDriveNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # When shutting down, stop all motors
        node.board.set_motor_duty([[1, 0], [2, 0], [3, 0], [4, 0]])
        node.get_logger().info("Shutting down MasterPi Drive Node, stopping motors.")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()