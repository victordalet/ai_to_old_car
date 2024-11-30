cmake_minimum_required(VERSION 3.0)
project(ai_old_car)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
set(CMAKE_CXX_STANDARD 17)

add_executable(ai_old_car main.cpp
        main.cpp)
target_link_libraries(ai_old_car ${OpenCV_LIBS})