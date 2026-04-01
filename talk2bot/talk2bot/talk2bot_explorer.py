import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from slam_toolbox.srv import SaveMap 
import subprocess
import random
import time

class SLAMExplorerNode(Node):
    def __init__(self):
        super().__init__('slam_explorer')
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan,
                                                 '/scan',
                                                 self.scan_callback,
                                                 10)
        self.safe_map_cli = self.create_client(SaveMap, '/slam_toolbox/save_map')
        self.obstacle_detected = False
        self.get_logger().info('Talk2Bot Explorer Mode Started. Mapping the environment...')

    def scan_callback(self, msg):
        # Check for obstacles in front of the robot
        front_ranges = msg.ranges[:30] + msg.ranges[-30:]  # Front 60 degrees
        # front_ranges = msg.ranges
        valid_ranges = [r for r in front_ranges if r > 0.1 and r < 1.0]  # Filter out invalid readings
        if valid_ranges and min(valid_ranges) < 0.4:
            self.obstacle_detected = True
        else:
            self.obstacle_detected = False
        
        self.move_robot()
    
    def move_robot(self):
        cmd = Twist()

        if self.obstacle_detected:
            # If an obstacle is detected, turn randomly
            self.get_logger().info('Obstacle detected! Turning to avoid...')
            cmd.linear.x = 0.0
            cmd.angular.z = random.choice([-0.5, 0.5])  # Turn left or right
        else:
            # Move forward if no obstacle is detected
            cmd.linear.x = 0.2
            cmd.angular.z = random.uniform(-0.1, 0.1)
        
        self.cmd_pub.publish(cmd)
    
    def safe_map(self, map_name="my_map"):
        # Save the map using the slam_toolbox service
        while not self.safe_map_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('SaveMap service not available, waiting...')
        
        request = SaveMap.Request()
        request.name.data = map_name

        self.get_logger().info(f'Sending service request to save map: {map_name}')
        future = self.safe_map_cli.call_async(request)

        future.add_done_callback(self.save_map_done_callback)
    
    def save_map_done_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info('Successfully saved map via slam_toolbox service!')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
    
def main(args=None):
    rclpy.init(args=args)
    explorer_node = SLAMExplorerNode()
    try:
        start_time = time.time()
        while rclpy.ok():
            rclpy.spin_once(explorer_node, timeout_sec=0.1)

            if time.time() - start_time > 60:
                explorer_node.get_logger().info('Exploration time limit reached. Stopping...')
                stop_cmd = Twist()
                explorer_node.cmd_pub.publish(stop_cmd)  # Stop the robot
                explorer_node.safe_map("talk2bot_map_demo")
                break
    except KeyboardInterrupt:
        explorer_node.get_logger().info('Interrupted by user. Saving map before exit...')
        explorer_node.safe_map("talk2bot_map_demo")
    finally:
        explorer_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()