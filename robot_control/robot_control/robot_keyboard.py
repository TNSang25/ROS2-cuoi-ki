#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import select
import termios
import tty

msg = """
=====================================
            ĐIỀU KHIỂN ROBOT 
=====================================
Sử dụng các phím sau để lái xe:
        W (Tiến)
A (Trái)  S (Dừng)  D (Phải)
        X (Lùi)

Nhấn CTRL-C để thoát.
"""

# Mapping từ phím bấm đến hướng di chuyển 
moveBindings = {
    'w': (1.0, 0.0),
    's': (0.0, 0.0),
    'x': (-1.0, 0.0),
    'a': (0.0, 1.0),
    'd': (0.0, -1.0),
}

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        # Tạo publisher cho topic cmd_vel
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # Tốc độ di chuyển và quay của robot
        self.linear_speed = 0.3   # 0.5 m/s 
        self.angular_speed = 0.5  # 0.75 rad/s 
        
    def publish_command(self, linear_dir, angular_dir):
        twist = Twist()
        # Tính toán tốc độ tuyến tính và góc quay dựa trên hướng di chuyển
        twist.linear.x = float(linear_dir * self.linear_speed)
        twist.angular.z = float(angular_dir * self.angular_speed)
        self.publisher_.publish(twist)

# Hàm đọc phím trực tiếp không cần nhấn Enter
def getKey(settings):
    tty.setraw(sys.stdin.fileno())
    # Đợi phím bấm trong 0.1s
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main(args=None):
    # Lưu lại trạng thái terminal
    settings = termios.tcgetattr(sys.stdin)
    
    rclpy.init(args=args)
    node = RobotController()
    
    print(msg)
    
    try:
        while rclpy.ok():
            key = getKey(settings)
            
            if key in moveBindings.keys():
                lin, ang = moveBindings[key]
                node.publish_command(lin, ang)
            elif key == '\x03': 
                break
                
    except Exception as e:
        print(f"Lỗi: {e}")
        
    finally:
        # Dừng robot khi thoát
        node.publish_command(0.0, 0.0)
        node.destroy_node()
        rclpy.shutdown()
        # Khôi phục trạng thái terminal ban đầu
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

if __name__ == '__main__':
    main()