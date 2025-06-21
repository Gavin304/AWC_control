from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
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

    # Sample pipeline arguments
    scanner_arg = DeclareLaunchArgument(
        name='scanner', default_value='scanner',
        description='Namespace for sample topics'
    )
    unilidar_arg = DeclareLaunchArgument(
        name='unilidar', default_value='unilidar',
        description='Namespace for input pointcloud topic'
    )

    # Static transforms (only one for map->cloud)
    static_tf_map_cloud = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0.3', '0', '1.2', '0', '3.14159', '0', 'map', 'cloud']
    )
    static_tf_cloud_imu = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'cloud', 'unilidar_imu_initial']
    )



    # Pointcloud to laserscan node (only one)
    sample_laserscan_node = Node(
        package='pointcloud_to_laserscan',
        executable='pointcloud_to_laserscan_node',
        remappings=[
            ('cloud_in', [LaunchConfiguration('unilidar'), '/cloud']),
            ('scan', [LaunchConfiguration('scanner'), '/scan'])
        ],
        parameters=[{
            'target_frame': 'cloud',
            'transform_tolerance': 0.01,
            'min_height': 0.5,
            'max_height': 1.2,
            'angle_min': -3.1416,
            'angle_max': 3.1416,
            'angle_increment': 0.00314,  # 0.1 degree in radians
            'scan_time': 0.1,
            'range_min': 0.5,
            'range_max': 10.0,
            'use_inf': True,
            'inf_epsilon': 1.0
        }],
        name='pointcloud_to_laserscan'
    )

    return LaunchDescription([
        scanner_arg,
        unilidar_arg,
        IncludeLaunchDescription(PythonLaunchDescriptionSource(unitree_launch)),
        static_tf_map_cloud,
        static_tf_cloud_imu,
        sample_laserscan_node
    ])