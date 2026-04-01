import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, Range
from slam_toolbox.srv import SaveMap 
import subprocess
import random
import time

class UltrasonicAvoidanceNode(Node):
    def __init__(self):
        super().__init__('ultrasonic_avoidance')
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.range_sub = self.create_subscription(Range,
                                                 '/ultrasonic_range',
                                                 self.range_callback,
                                                 10)
        self.get_logger().info('Talk2Bot Explorer Mode Started.')
        self.stop_distance = 0.4
        self.is_turning = False

    def range_callback(self, msg):
        current_range = msg.range
        cmd = Twist()

        if current_range < self.stop_distance and current_range > msg.min_range:
            self.get_logger().warn(f'Obstacle detected at {current_range:.2f} meters! Stopping and turning...')
            cmd.linear.x = 0.0
            cmd.angular.z = 0.8 if not self.is_turning else 0.8
            self.is_turning = True
        else:
            cmd.linear.x = 0.15
            cmd.angular.z = 0.0
            self.is_turning = False
        
        self.cmd_pub.publish(cmd)
            
def main(args=None):
    rclpy.init(args=args)
    node = UltrasonicAvoidanceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        stop_cmd = Twist()
        node.cmd_pub.publish(stop_cmd)
        node.get_logger().info('Shutting down Talk2Bot Explorer Mode. Stopping the robot...')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()