#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu

class ImuReader(Node):
    def __init__(self):
        super().__init__('imu_reader_node')
        
        # Tạo subscription để đọc dữ liệu IMU từ topic /imu/data
        self.subscription = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10
        )
        self.subscription  # Tránh cảnh báo biến không sử dụng
        
        self.get_logger().info('Đang chờ dữ liệu...')

    def imu_callback(self, msg):
        # Đọc gia tốc tuyến tính (m/s^2)
        accel_x = msg.linear_acceleration.x
        accel_y = msg.linear_acceleration.y
        accel_z = msg.linear_acceleration.z
        
        # Đọc tốc độ góc (rad/s)
        gyro_x = msg.angular_velocity.x
        gyro_y = msg.angular_velocity.y
        gyro_z = msg.angular_velocity.z
        
        # Đọc hướng quay (quaternion)
        qx = msg.orientation.x
        qy = msg.orientation.y
        qz = msg.orientation.z
        qw = msg.orientation.w

        # In ra terminal
        self.get_logger().info(
            f'Gia tốc m/s^2 (X,Y,Z): [{accel_x:.2f}, {accel_y:.2f}, {accel_z:.2f}] | '
            f'Gyro rad/s (X,Y,Z): [{gyro_x:.2f}, {gyro_y:.2f}, {gyro_z:.2f}]'
        )

def main(args=None):
    rclpy.init(args=args)
    node = ImuReader()
    
    try:
        rclpy.spin(node) # Giữ node chạy liên tục để nhận dữ liệu
    except KeyboardInterrupt:
        node.get_logger().info('Đã dừng node.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()