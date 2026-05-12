import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Thay 'your_package_name' bằng tên package của bạn
    pkg_dir = get_package_share_directory('robot_cartographer_3d')
    config_dir = os.path.join(pkg_dir, 'config')

    return LaunchDescription([
        # 1. Node Cartographer chính
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': True}], # Để True nếu chạy trong Gazebo mô phỏng
            arguments=[
                '-configuration_directory', config_dir,
                '-configuration_basename', 'cartographer_3d.lua'
            ],
            remappings=[
                ('/points2', '/velodyne_points'), # Remap lại tên topic PointCloud2 của bạn
                ('/imu', '/imu/data')             # Remap lại tên topic IMU của bạn
            ]
        ),

        # 2. Node xuất bản đồ 2D Occupancy Grid (cho Nav2)
        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='cartographer_occupancy_grid_node',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'resolution': 0.05, # Độ phân giải bản đồ (5cm/pixel)
                'publish_period_sec': 1.0
            }]
        ),
    ])