from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[{
                # --- Core Configuration ---
                'use_scan_matching': True,
                'use_imu_data': False,
                'use_sim_time': False,

                # --- Frame and Topic Configuration ---
                'odom_frame': 'odom',
                'map_frame': 'map',
                'base_frame': 'base_link',
                'scan_topic': '/scan',
                'imu_topic': '/unilidar/imu',

                # --- Sensor-Specific Parameters ---
                'min_laser_range': 0.55,  # ← lower this below your lidar’s true min
                'max_laser_range': 10.0,
                'transform_timeout': 2.0,
                'transform_tolerance': 2.0,
                'transform_publish_period': 0.02,
                'tf_message_filter_queue_size': 500,

                # --- Performance and Tuning Parameters ---
                'resolution': 0.05,
                'map_update_interval': 1.5,
                'scan_buffer_size': 20,
                'tf_buffer_duration': 30.0,
                'transform_publish_period': 0.05,

                # --- Scan Matching Tuning ---
                'distance_variance_penalty': 0.4, # Lower = rely more on odom
                'angle_variance_penalty': 0.8,    # Lower = rely more on odom
                'translation_weight': 1.0,
                'rotation_weight': 1.0,
                'use_scan_barycenter': True,

                # --- Solver Parameters ---
                'solver_parameters': {
                    'minimum_time_interval': 0.0
                },

                # --- Humble-Compatible QoS Fix ---
                'scan_qos': 'sensor_data',
                'tf_qos': 'sensor_data',
                'scan_subscription_qos': 'reliable',
                'tf_subscription_qos': 'reliable',
            }],
        )
    ])