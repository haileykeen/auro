import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
import time

class SimpleScanPub(Node):
    def __init__(self):
        super().__init__('sim_scan_node')
        self.publisher_ = self.create_publisher(LaserScan, '/scan', 10)
        timer_period = 0.5  # 2Hz
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'map' # 這裡暫時設為 map
        msg.angle_min = -1.57
        msg.angle_max = 1.57
        msg.angle_increment = 0.314
        msg.range_min = 0.0
        msg.range_max = 10.0
        msg.ranges = [1.0, 2.0, 5.0, 2.0, 1.0, 0.5, 3.0, 1.0, 1.0, 1.0, 1.0] # 隨便給點數值
        
        self.publisher_.publish(msg)
        self.get_logger().info('正在發送 /scan 數據...')

def main(args=None):
    rclpy.init(args=args)
    node = SimpleScanPub()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()