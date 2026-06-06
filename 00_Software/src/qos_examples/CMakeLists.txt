cmake_minimum_required(VERSION 3.8)
project(qos_examples)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# --- C++ Node Configuration ---
add_executable(qos_publisher src/qos_publisher.cpp)
ament_target_dependencies(qos_publisher
  rclcpp
  std_msgs
)

# Install C++ executables
install(TARGETS
  qos_publisher
  DESTINATION lib/${PROJECT_NAME}
)

# --- Python Node Configuration ---
# Automatically make the python script executable during build/configuration
execute_process(
  COMMAND chmod +x ${CMAKE_CURRENT_SOURCE_DIR}/scripts/qos_subscriber.py
)

# Install Python scripts as programs
install(PROGRAMS
  scripts/qos_subscriber.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files and config files (if any)
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
