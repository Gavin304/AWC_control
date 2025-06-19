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
        'launch.py' # Make sure this is the correct launch file from the package
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
    static_tf_base_to_lidar_frame = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=[
            '0.3', '0', '1.2',  # X, Y, Z offset from base_link to the lidar
            '0', '0', '0',      # Roll, Pitch, Yaw offset
            'base_link',        # Parent Frame
            'unilidar_lidar'    # Child Frame (This is a common choice, verify from the sensor's docs/TF tree)
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
            # ✅ The target_frame should match the 'child frame' of your static transform.
            'target_frame': 'unilidar_lidar',
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
        # Do NOT include odom_to_base_node here.
        static_tf_base_to_lidar_frame, # Use the single, correct static transform.
        IncludeLaunchDescription(PythonLaunchDescriptionSource(unitree_launch)),
        pointcloud_to_laserscan_node
    ])