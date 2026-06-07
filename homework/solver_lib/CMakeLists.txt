cmake_minimum_required(VERSION 3.10)
project(solver_lib VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Создаем статическую библиотеку solver
add_library(solver STATIC ${CMAKE_CURRENT_SOURCE_DIR}/solver.cpp)

# Указываем директорию с заголовочными файлами
target_include_directories(solver PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Установка
install(TARGETS solver
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin)

install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/solver.h
        DESTINATION include)
