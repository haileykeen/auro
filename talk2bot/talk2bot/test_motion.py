import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time

class MotionTester(Node):
    def __init__(self):
        super().__init__('motion_tester')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.get_logger().info('開始動作一致性測試...')

    def send_cmd(self, x=0.0, y=0.0, z=0.0, duration=1.0):
        msg = Twist()
        msg.linear.x = float(x)
        msg.linear.y = float(y)
        msg.angular.z = float(z)
        
        # keep sending for a time
        end_time = time.time() + duration
        while time.time() < end_time:
            self.publisher.publish(msg)
            time.sleep(0.1)
        
        # Stop after move
        self.publisher.publish(Twist())
        time.sleep(1.0)

def main():
    rclpy.init()
    tester = MotionTester()

    try:
        tester.get_logger().info('Test1: move forward 1s')
        tester.send_cmd(x=0.3, duration=3.0)

        tester.get_logger().info('Test2: move ')
        tester.send_cmd(y=0.3, duration=3.0)

        tester.get_logger().info('Test3: turn left')
        tester.send_cmd(z=0.5, duration=3.0)

        tester.get_logger().info('test done')

    except KeyboardInterrupt:
        tester.publisher.publish(Twist())
    finally:
        tester.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()