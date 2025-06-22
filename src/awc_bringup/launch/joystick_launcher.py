from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, TimerAction

def generate_launch_description():
    serial_port_arg = DeclareLaunchArgument(
        'serial_port', default_value='/dev/ttyUSB0',
        description='Serial port for Arduino'
    )
    wheel_radius_arg = DeclareLaunchArgument(
        'wheel_radius', default_value='0.1651',
        description='Wheel radius in meters'
    )

    joystick_node = Node(
        package='joystick_ros2',
        executable='joystick_ros2',
        name='joystick_ros2_node',
        output='screen'
    )

    js2fork_node = Node(
        package='js2fork',
        executable='js2fork',
        name='js2fork',
        output='screen'
    )

    ros2arduino_node = Node(
        package='ros2arduino',
        executable='ros2arduino',
        name='ros2arduino',
        output='screen',
        parameters=[
            {'serial_port': LaunchConfiguration('serial_port')},
            {'wheel_radius': LaunchConfiguration('wheel_radius')}
        ]
    )

    delayed_nodes = TimerAction(
        period=2.0,
        actions=[js2fork_node, ros2arduino_node]
    )

    return LaunchDescription([
        serial_port_arg,
        wheel_radius_arg,
        joystick_node,
        delayed_nodes
    ])