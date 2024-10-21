cmake_minimum_required(VERSION 3.0)
project(ai_to_old_car)

set(project_name ai_to_old_car)

find_package(OpenCV REQUIRED)


find_path(ONNXRUNTIME_INCLUDE_DIR onnxruntime_c_api.h
        HINTS /home/victor/Documents/other/onnxruntime-linux-x64-1.19.2/include
)
find_library(ONNXRUNTIME_LIBRARY onnxruntime
        HINTS /home/victor/Documents/other/onnxruntime-linux-x64-1.19.2/lib
)


add_library(${project_name}-lib
        src/yolo.cpp
        src/yolo.h
)

target_include_directories(${project_name}-lib PUBLIC src)
target_include_directories(${project_name}-lib PUBLIC ${ONNXRUNTIME_INCLUDE_DIR})

target_link_libraries(${project_name}-lib
        PUBLIC ${OpenCV_LIBS}
        PUBLIC ${ONNXRUNTIME_LIBRARY}
)

# Add the main executable
add_executable(${project_name}
        main.cpp
)
target_include_directories(${project_name} PUBLIC ${ONNXRUNTIME_INCLUDE_DIR})
target_link_libraries(${project_name} ${project_name}-lib)

