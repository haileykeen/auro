import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, JointState
from geometry_msgs.msg import Twist

import os
import math

class VLMTaskNode(Node):
    def __init__(self):
        super().__init__('talk2bot_manager')
        self.image_sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.joint_state_sub = self.create_subscription(JointState, '/joint_states', self.joint_state_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.current_joints = [0.0] * 5

        self.get_logger().info('Talk2Bot ROS2 Node has started!')

        def image_callback(self, msg):
            pass
        def joint_state_callback(self, msg):
            self.current_joints = msg.position
            degrees = [round(math.degrees(a), 2) for a in self.current_joints]
            
            self.get_logger().info(f'Monitoring Angles (deg): {degrees}')

            self.calculate_forward_kinematics()
        
        def calculate_forward_kinematics(self):
            if len(self.current_joints) < 3:


