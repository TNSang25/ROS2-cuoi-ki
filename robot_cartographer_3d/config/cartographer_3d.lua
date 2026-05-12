include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",
  -- TRONG 3D, TRACKING FRAME PHẢI LÀ IMU FRAME
  tracking_frame = "imu_link", 
  published_frame = "base_footprint",
  odom_frame = "odom",
  provide_odom_frame = true, -- Bật false nếu bạn đã có node publish odom riêng
  publish_frame_projected_to_2d = false,
  use_pose_extrapolator = true,
  
  -- Thiết lập cảm biến
  use_odometry = true, -- Bật true nếu có odom từ encoder
  use_nav_sat = false,
  use_landmarks = false,
  num_laser_scans = 0, -- Tắt 2D LiDAR
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 1, -- BẬT 1 ĐỂ DÙNG 3D POINT CLOUD
  
  -- Cấu hình tần số publish
  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,
  rangefinder_sampling_ratio = 1.,
  odometry_sampling_ratio = 1.,
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 1.,
  landmarks_sampling_ratio = 1.,
}

-- CHỈ ĐỊNH DÙNG TRAJECTORY BUILDER 3D
MAP_BUILDER.use_trajectory_builder_3d = true
MAP_BUILDER.num_background_threads = 4 -- Tùy số luồng CPU của bạn

-- Tinh chỉnh bộ lọc Point Cloud 3D (giảm tải CPU)
TRAJECTORY_BUILDER_3D.voxel_filter_size = 0.15
TRAJECTORY_BUILDER_3D.submaps.high_resolution = 0.10
TRAJECTORY_BUILDER_3D.submaps.low_resolution = 0.45

return options