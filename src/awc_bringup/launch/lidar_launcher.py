from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Path to the unitree lidar launch file
    unitree_launch = os.path.join(
        get_package_share_directory('unitree_lidar_ros2'),
        'launch',
        'launch.py'
    )

    # Arguments for remapping topics, if needed
    scanner_arg = DeclareLaunchArgument(
        name='scanner', default_value='scanner',
        description='Namespace for sample topics'
    )
    unilidar_arg = DeclareLaunchArgument(
        name='unilidar', default_value='unilidar',
        description='Namespace for input pointcloud topic'
    )

    # --- TF SECTION ---

    # 1. Publishes odom -> base_link (from your wheel odometry)
    #    NOTE: Check your setup.py for the correct executable name. I'm assuming 'awc_controller'.
    odom_to_base_node = Node(
        package='tf_publisher',
        executable='tf_broadcaster', #<-- CHECK THIS NAME
        name='awc_odometry_node',
        output='screen'
    )


    static_tf_sensor_imu = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '--x', '0.3',
            '--y', '0',
            '--z', '1.2',
            '--roll', '3.14159',
            '--pitch', '0',
            '--yaw', '0',
            '--frame-id', 'base_link',
            '--child-frame-id', 'unilidar_imu_initial'
        ]
    )

    static_tf_virtual_lidar = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '--x', '0',
            '--y', '0',
            '--z', '0',
            '--roll', '-3.14159',
            '--pitch', '0',
            '--yaw', '0',
            '--frame-id', 'unilidar_imu_initial',
            '--child-frame-id', 'unilidar_imu_upright'
        ]
    )

    # --- DATA PROCESSING SECTION ---
    
    # Pointcloud to laserscan node
    # It converts the 3D PointCloud from the sensor into a 2D LaserScan
    pointcloud_to_laserscan_node = Node(
        package='pointcloud_to_laserscan',
        executable='pointcloud_to_laserscan_node',
        name='pointcloud_to_laserscan',
        remappings=[
            # The input cloud topic from the unitree_lidar driver
            ('cloud_in', [LaunchConfiguration('unilidar'), '/cloud']),
            # The output 2D scan topic
            ('scan', [LaunchConfiguration('scanner'), '/scan'])
        ],
        parameters=[{
            # IMPORTANT: The target frame for the 2D scan should be the robot's base.
            'target_frame': 'unilidar_imu_upright',
            'transform_tolerance': 0.05, # Increased tolerance slightly for real hardware
            'min_height': 0.5, # Set a wide range, then narrow down based on what you see
            'max_height': 1.2,
            'angle_min': -3.14159,
            'angle_max': 3.14159,
            'angle_increment': 0.0087,  # 0.5 degrees, a more realistic value
            'scan_time': 0.1,
            'range_min': 0.5,
            'range_max': 10.0,
            'use_inf': True
        }]
    )

    return LaunchDescription([
        scanner_arg,
        unilidar_arg,
        
        # Start all the TF publishers
        odom_to_base_node,
        static_tf_sensor_imu,
        static_tf_virtual_lidar,
        
        # Start the sensor driver
        IncludeLaunchDescription(PythonLaunchDescriptionSource(unitree_launch)),
        
        # Start the conversion node
        pointcloud_to_laserscan_node
    ])