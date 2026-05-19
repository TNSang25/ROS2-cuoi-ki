import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
import csv
import time

class PositionLogger(Node):
    def __init__(self):
        super().__init__('position_logger_node')
        
        # Subscriber nhận Vị trí thực (Ground Truth)
        self.subscription = self.create_subscription(
            Odometry,
            '/odom', 
            self.gt_callback,
            10)
        self.latest_gt_msg = None

        # Thiết lập TF để lấy Vị trí ước lượng (Estimated Position)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Mở file CSV và chỉ ghi Header với cột x, y
        self.csv_file = open('position_log_2d.csv', mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['timestamp', 'true_x', 'true_y', 'est_x', 'est_y'])

        # Timer chạy mỗi 5 giây
        self.timer_period = 5.0
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        self.get_logger().info('Bắt đầu ghi tọa độ 2D (x,y) mỗi 5 giây...')

    def gt_callback(self, msg):
        self.latest_gt_msg = msg

    def timer_callback(self):
        if self.latest_gt_msg is None:
            self.get_logger().warn('Chưa nhận được dữ liệu Ground Truth...')
            return

        # Chỉ lấy x, y từ Vị trí thực
        true_x = self.latest_gt_msg.pose.pose.position.x
        true_y = self.latest_gt_msg.pose.pose.position.y

        try:
            # Tra cứu TF từ map -> base_footprint
            t = self.tf_buffer.lookup_transform(
                'map',
                'base_footprint',
                rclpy.time.Time())
            
            # Chỉ lấy x, y từ Vị trí ước lượng
            est_x = t.transform.translation.x
            est_y = t.transform.translation.y

        except TransformException as ex:
            self.get_logger().info(f'Chưa lấy được TF: {ex}')
            return

        # Lấy thời gian hiện tại
        current_time = time.time()

        # Ghi một hàng dữ liệu (chỉ gồm x, y) vào file CSV
        self.csv_writer.writerow([current_time, true_x, true_y, est_x, est_y])
        self.get_logger().info(f'Đã ghi: True({true_x:.2f}, {true_y:.2f}) | Est({est_x:.2f}, {est_y:.2f})')

    def destroy_node(self):
        self.csv_file.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    position_logger = PositionLogger()
    
    try:
        rclpy.spin(position_logger)
    except KeyboardInterrupt:
        pass
    finally:
        position_logger.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()