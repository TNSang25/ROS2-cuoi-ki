# Cần có
* [**ROS 2 Humble**](https://docs.ros.org/en/humble/index.html)

* [**Ignition Gazebo**](https://docs.ros.org/en/foxy/Tutorials/Advanced/Simulators/Ignition/Ignition.html)
```
sudo apt install ignition-fortress -y
```

* **ROS 2 - Ignition Bridge**
```
sudo apt install ros-humble-ros-gz -y
```

# Các Packages và chức năng
* [**gazebo_map**](gazebo_map) : tạo không gian mô phỏng (world) cho Robot trong Gazebo.
* [**my_robot_description**](my_robot_description) : tạo Robot với các folder urdf và meshes.
* [**robot_bringup**](robot_bringup) : mở bản đồ và spawn Robot, chứa file cấu hình bridge ROS2-Gazebo.
* [**robot_control**](robot_control) : chứa các node điều khiển các khớp tay máy, lái xe, và node đọc dữ liệu IMU.
* [**robot_cartographer_2d**](robot_cartographer_2d) : cấu hình và chạy thuật toán Cartographer 2D.
* [**robot_slam_toolbox**](robot_slam_toolbox) : cấu hình và chạy thuật toán SLAM Toolbox.
# Clone repo
```
https://github.com/TNSang25/ROS2-cuoi-ki.git
```
# Các bước chạy
**Mở bản đồ và spawn Robot** :

```
# File launch với tham số world là các map(map1.sdf, map2.sdf, map3.sdf)
ros2 launch robot_bringup robot_gazebo.launch.xml world:=map1.sdf
```

**Chạy thuật toán SLAM**:
* SLAM Toolbox :
```
source install/setup.bash
ros2 launch robot_slam_toolbox karto.launch.py
```

* Cartographer 2D :
```
source install/setup.bash
ros2 launch robot_cartographer_2d cartographer.launch.py 
```

**Chạy node lái robot** :
```
source install/setup.bash
ros2 run robot_control robot_keyboard
```
