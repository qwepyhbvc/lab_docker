cmake_minimum_required(VERSION 3.10)
project(hello_world_app VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Исполняемый файл
add_executable(hello_world ${CMAKE_CURRENT_SOURCE_DIR}/hello_world.cpp)

# Линковка (без add_subdirectory)
target_link_libraries(hello_world PRIVATE formatter_ex)

# Установка
install(TARGETS hello_world
        RUNTIME DESTINATION bin)
