import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import math
import time

class ArmManager(Node):
    def __init__(self):
        super().__init__('arm_manager')
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.l1, self.l2, self.l3, self.l4 = 96.0, 105.0, 105.0, 80.0 # Link lengths in mm
        self.get_logger().info('MasterPi Arm Manager with FK is ready!')

    def calculate_fk(self, q):
        r = (self.l2 * math.sin(q[1]) + 
             self.l3 * math.sin(q[1] + q[2]) + 
             self.l4 * math.sin(q[1] + q[2] + q[3]))
        
        x = r * math.cos(q[0])
        y = r * math.sin(q[0])
        z = (self.l1 + 
             self.l2 * math.cos(q[1]) + 
             self.l3 * math.cos(q[1] + q[2]) + 
             self.l4 * math.cos(q[1] + q[2] + q[3]))
        
        return x, y, z
    
    def move_to_joints(self, j1, j2, j3, j4, gripper_pos):
        angles = [float(j1), float(j2), float(j3), float(j4)]
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['joint1', 'joint2', 'joint3', 'joint4', 'gripper']
        msg.position = angles + [float(gripper_pos)]

        x, y, z = self.calculate_fk(angles)
        self.get_logger().info(f"Targeting -> X: {x:.1f}, Y: {y:.1f}, Z: {z:.1f} (mm)")
        self.get_logger().info(f"Joints -> {angles}")

        self.joint_pub.publish(msg)
    
    def sequence_stow(self):
        self.get_logger().info('Action: Stowing Arm for Navigation...')
        self.move_to_joints(0.0, -1.5, 1.5, 0.0, 1.0) #NEED TO ADJUST

    
    def pick_up_sequence(self):
        self.get_logger().info('--- Starting Pick-up Sequence ---')
        # Initial approach to the ball #####NEED TO ADJUST#####
        self.move_to_joints(0.0, 0.5, -0.5, 0.0, 0.0)
        time.sleep(2)  # Wait for the arm to move
        self.move_to_joints(0.0, 0.7, -0.6, 0.0, 0.0) # Move closer to the ball
        time.sleep(1)
        self.move_to_joints(0.0, 0.7, -0.6, 0.0, 1.0) # Close gripper to pick up
        time.sleep(1)
        self.move_to_joints(0.0, 0.0, 0.0, 0.0, 1.0) # Lift the ball up
        self.get_logger().info('Pick-up Sequence Complete.')
    
def main():
    rclpy.init()
    node = ArmManager()
        
    try:
        node.sequence_stow()
        time.sleep(2.0)
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

