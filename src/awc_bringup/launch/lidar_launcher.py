from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    unitree_launch = os.path.join(
        get_package_share_directory('unitree_lidar_ros2'),
        'launch',
        'launch.py'
    )

    scanner_arg = DeclareLaunchArgument(
        name='scanner', default_value='scanner',
        description='Namespace for sample topics'
    )
    unilidar_arg = DeclareLaunchArgument(
        name='unilidar', default_value='unilidar',
        description='Namespace for input pointcloud topic'
    )

    # --- TF SECTION ---

    odom_to_base_node = Node(
        package='tf_publisher',
        executable='tf_broadcaster',
        name='awc_odometry_node',
        output='screen'
    )

    static_tf_base_to_imu_initial = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0.3', '0', '1.2',
            '0', '0', '0',
            'base_link',
            'unilidar_imu_initial'
        ]
    )

    # ✅ Final fix: base_link → unilidar_imu (direct, to avoid filter drop)
    static_tf_base_to_imu_direct = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0.3', '0', '1.2',
            '0', '0', '0',
            'base_link',
            'unilidar_imu'
        ]
    )

    pointcloud_to_laserscan_node = Node(
        package='pointcloud_to_laserscan',
        executable='pointcloud_to_laserscan_node',
        name='pointcloud_to_laserscan',
        remappings=[
            ('cloud_in', [LaunchConfiguration('unilidar'), '/cloud']),
            ('scan', '/scan')
        ],
        parameters=[{
            'target_frame': 'unilidar_imu',
            'transform_tolerance': 0.05,
            'min_height': 0.5,
            'max_height': 1.2,
            'angle_min': -3.14159,
            'angle_max': 3.14159,
            'angle_increment': 0.0087,
            'scan_time': 0.1,
            'range_min': 0.56,
            'range_max': 10.0,
            'use_inf': True
        }]
    )

    return LaunchDescription([
        scanner_arg,
        unilidar_arg,
        odom_to_base_node,
        static_tf_base_to_imu_initial,
        static_tf_base_to_imu_direct, 
        IncludeLaunchDescription(PythonLaunchDescriptionSource(unitree_launch)),
        pointcloud_to_laserscan_node
    ])
