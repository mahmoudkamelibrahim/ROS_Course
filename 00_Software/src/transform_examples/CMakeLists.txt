cmake_minimum_required(VERSION 3.8)
project(transform_examples)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(launch_testing_ament_cmake REQUIRED)

add_executable(static_broadcaster src/static_broadcaster.cpp)
ament_target_dependencies(static_broadcaster rclcpp tf2 tf2_ros geometry_msgs)

install(TARGETS static_broadcaster DESTINATION lib/${PROJECT_NAME})

# Install the launch directory
install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch)

ament_package()
