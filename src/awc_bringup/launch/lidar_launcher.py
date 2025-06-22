from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, TimerAction
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
    wheel_radius_arg = DeclareLaunchArgument(
        'wheel_radius', default_value='0.1651',
        description='Wheel radius in meters'
    )
    wheel_separation_arg = DeclareLaunchArgument(
        'wheel_separation', default_value='0.46',
        description='Wheel separation in meters'
    )

    tf_broadcaster_node = Node(
        package='tf_publisher',
        executable='tf_broadcaster',
        name='awc_controller',
        output='screen',
        parameters=[
            {'wheel_radius': LaunchConfiguration('wheel_radius')},
            {'wheel_separation': LaunchConfiguration('wheel_separation')}
        ]
    )

    static_tf_base_to_imu_initial = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0.3', '0', '1.2',
            '0', '0', '3.14159',
            'base_link',
            'unilidar_imu_initial'
        ]
    )

    # --- Pointcloud to Laserscan ---
    pointcloud_to_laserscan_node = Node(
        package='pointcloud_to_laserscan',
        executable='pointcloud_to_laserscan_node',
        name='pointcloud_to_laserscan',
        remappings=[
            ('cloud_in', [LaunchConfiguration('unilidar'), '/cloud']),
            ('scan', '/scan')
        ],
        parameters=[{
            'target_frame': 'base_link',
            'transform_tolerance': 0.5,
            'min_height': 0.5,
            'max_height': 1.2,
            'angle_min': -3.14159,
            'angle_max': 3.14159,
            'angle_increment': 0.0087,
            'scan_time': 0.1,
            'range_min': 0.55,
            'range_max': 10.0,
            'use_inf': True,
            'override_frame_id': 'base_link',
            'override_laser_scan_time': True
        }]
    )



    return LaunchDescription([
        scanner_arg,
        unilidar_arg,
        wheel_radius_arg,
        wheel_separation_arg,
        tf_broadcaster_node,
        static_tf_base_to_imu_initial,
        IncludeLaunchDescription(PythonLaunchDescriptionSource(unitree_launch)),
        pointcloud_to_laserscan_node,
    ])
