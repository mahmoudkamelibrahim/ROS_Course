cmake_minimum_required(VERSION 3.8)
project(hybrid_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

# --- C++ Node Configuration ---
add_executable(cpp_publisher src/cpp_publisher.cpp)
ament_target_dependencies(cpp_publisher
  rclcpp
  std_msgs
)

# Install C++ executables
install(TARGETS
  cpp_publisher
  DESTINATION lib/${PROJECT_NAME}
)

# --- Python Node Configuration ---
# Automatically make the python script executable during build/configuration
execute_process(
  COMMAND chmod +x ${CMAKE_CURRENT_SOURCE_DIR}/scripts/py_subscriber.py
)

# Install Python scripts as programs so they are marked as executable and put in the target's bin path
install(PROGRAMS
  scripts/py_subscriber.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()

