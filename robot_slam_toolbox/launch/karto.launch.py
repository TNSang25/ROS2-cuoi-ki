import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node  # [THÊM MỚI] Import thư viện gọi Node

def generate_launch_description():
    # 1. Lấy đường dẫn dạng string chuẩn
    karto_pkg_dir = get_package_share_directory('robot_slam_toolbox')
    slam_toolbox_dir = get_package_share_directory('slam_toolbox')

    # 2. Tạo đường dẫn tới file config của thuật toán SLAM
    slam_config_path = os.path.join(
        karto_pkg_dir,
        'config',
        'karto_params.yaml'
    )

    # 3. [THÊM MỚI] Tạo đường dẫn tới file cấu hình giao diện RViz2
    rviz_config_path = os.path.join(
        karto_pkg_dir,
        'rviz',
        'config.rviz'
    )

    # 4. Gọi file launch của slam_toolbox
    start_slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(slam_toolbox_dir, 'launch', 'online_async_launch.py')
        ),
        launch_arguments={'slam_params_file': slam_config_path}.items()
    )

    # 5. [THÊM MỚI] Khởi tạo Node RViz2 và nạp file cấu hình
    start_rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        output='screen'
    )

    # 6. Thêm cả 2 tiến trình vào Launch Description
    return LaunchDescription([
        start_slam_toolbox,
        start_rviz2   # [THÊM MỚI]
    ])