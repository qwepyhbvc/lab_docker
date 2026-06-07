cmake_minimum_required(VERSION 3.10)
project(formatter_lib VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Создаем статическую библиотеку
add_library(formatter STATIC ${CMAKE_CURRENT_SOURCE_DIR}/formatter.cpp)

# Указываем директорию с заголовочными файлами
target_include_directories(formatter PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Установка библиотеки и заголовочного файла
install(TARGETS formatter
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin)

install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/formatter.h
        DESTINATION include)
