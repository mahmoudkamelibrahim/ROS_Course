cmake_minimum_required(VERSION 3.8)
project(hello_ros2)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

# Add executable
add_executable(hello_node src/hello_node.cpp)
target_include_directories(hello_node PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)

# Add dependencies to the executable
ament_target_dependencies(hello_node rclcpp)

# Install executable
install(TARGETS hello_node
  DESTINATION lib/${PROJECT_NAME})

ament_package()
