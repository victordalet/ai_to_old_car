cmake_minimum_required(VERSION 3.0)
project(ai_to_old_car)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
set(CMAKE_CXX_STANDARD 20)

add_executable(ai_to_old_car main.cpp)
target_link_libraries(ai_to_old_car ${OpenCV_LIBS})
