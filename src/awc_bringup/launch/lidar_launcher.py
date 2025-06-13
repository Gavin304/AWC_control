from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Paths to the other launch files
    unitree_launch = os.path.join(
        get_package_share_directory('unitree_lidar_ros2'),
        'launch',
        'launch.py'
    )
    pcl2scan_launch = os.path.join(
        get_package_share_directory('pointcloud_to_laserscan'),
        'launch',
        'sample_pointcloud_to_laserscan_launch.py'
    )

    static_tf_map_cloud = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0.3', '0', '1', '0', '0', '0', '1', 'map', 'cloud']
    )
    static_tf_cloud_imu = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', '1', 'cloud', 'unilidar_imu_initial']
    )

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(unitree_launch)
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(pcl2scan_launch)
        ),
        static_tf_map_cloud,
        static_tf_cloud_imu
    ])