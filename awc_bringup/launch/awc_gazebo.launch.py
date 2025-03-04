import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    robotXacroName = 'awc_robot'

    namePackage = 'awc_description'
    modelFileRelativePath = 'awc_robot/robot.urdf.xacro'
    worldFileRelativePath = 'worlds/awc_empty.world'