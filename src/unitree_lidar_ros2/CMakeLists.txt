cmake_minimum_required(VERSION 3.5)

# Set CMP0074 policy to NEW to allow find_package to use <PackageName>_ROOT variables
cmake_policy(SET CMP0074 NEW)

project(unitree_lidar_ros2)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

set(CMAKE_SKIP_RPATH TRUE)
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
set(CMAKE_INSTALL_RPATH "/usr/lib/x86_64-linux-gnu")

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(pcl_conversions REQUIRED)
find_package(PCL REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(sensor_msgs REQUIRED)

include_directories(
  ${PCL_INCLUDE_DIRS}
  include
  ../unitree_lidar_sdk/include  # Adjusted to use a relative path
)

link_directories(
  ${PCL_LIBRARY_DIRS}
  ../unitree_lidar_sdk/lib/${CMAKE_SYSTEM_PROCESSOR}  # Adjusted to use a relative path
)

add_definitions(${PCL_DEFINITIONS})

add_executable(unitree_lidar_ros2_node src/unitree_lidar_ros2_node.cpp)

target_link_libraries( unitree_lidar_ros2_node
  ${Boost_SYSTEM_LIBRARY}
  ${PCL_LIBRARIES}
  libunitree_lidar_sdk.a
)

ament_target_dependencies(
  unitree_lidar_ros2_node
  rclcpp std_msgs 
  sensor_msgs
  geometry_msgs 
  tf2_ros
  pcl_conversions
)

install(TARGETS
unitree_lidar_ros2_node
  DESTINATION lib/${PROJECT_NAME}
)

# install rviz file and launch file
install(FILES
  launch/launch.py
  DESTINATION share/${PROJECT_NAME}/launch
)
install(FILES
  rviz/view.rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
