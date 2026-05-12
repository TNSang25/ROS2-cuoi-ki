#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import sys
import select
import termios
import tty

# Hướng dẫn hiển thị trên terminal
msg = """
ĐIỀU KHIỂN TAY MÁY BẰNG BÀN PHÍM
---------------------------
Khớp 1 (Quay):
   w : Tăng góc (+0.1 rad)
   s : Giảm góc (-0.1 rad)

Khớp 2 (Trượt):
   a : Xuống (+0.05 m)
   d : Lên (-0.05 m)

q hoặc Ctrl+C để thoát!
"""

# Hàm đọc phím 
def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

class ArmController(Node):
    def __init__(self):
        super().__init__('arm_controller')
        
        # Tạo publisher 
        self.pub_link1 = self.create_publisher(Float64, '/link1_cmd_pos', 10)
        self.pub_link2 = self.create_publisher(Float64, '/link2_cmd_pos', 10)
        
        # Biến lưu vị trí hiện tại 
        self.pos_link1 = 0.0
        self.pos_link2 = 0.0
        
        # Bước nhảy cho mỗi lần nhấn phím
        self.step_rot = 0.1   
        self.step_lin = 0.05  

    def publish_positions(self):
        msg1 = Float64()
        msg1.data = self.pos_link1
        self.pub_link1.publish(msg1)
        
        msg2 = Float64()
        msg2.data = self.pos_link2
        self.pub_link2.publish(msg2)

def main(args=None):
    # Lưu cài đặt terminal hiện tại
    settings = termios.tcgetattr(sys.stdin)
    
    rclpy.init(args=args)
    node = ArmController()
    
    print(msg)
    
    try:
        while rclpy.ok():
            key = get_key(settings)
            
            if key != '':
                if key == 'w':
                    node.pos_link1 += node.step_rot
                elif key == 's':
                    node.pos_link1 -= node.step_rot
                elif key == 'a':
                    node.pos_link2 += node.step_lin
                elif key == 'd':
                    node.pos_link2 -= node.step_lin
                elif key == 'q' or key == '\x03': # \x03 là Ctrl+C
                    break
                
                # In ra trạng thái hiện tại
                print(f"\rKhớp 1 (Quay): {node.pos_link1:.2f} rad | Khớp 2 (Trượt): {node.pos_link2:.2f} m", end='')
                
                # Gửi lệnh đi
                node.publish_positions()
                
    except Exception as e:
        print(e)
    finally:
        # Khôi phục cài đặt terminal
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()