from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import TimerAction

def generate_launch_description():
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
        output='screen'
    )

    delayed_nodes = TimerAction(
        period=2.0,
        actions=[js2fork_node, ros2arduino_node]
    )

    return LaunchDescription([
        joystick_node,
        delayed_nodes
    ])