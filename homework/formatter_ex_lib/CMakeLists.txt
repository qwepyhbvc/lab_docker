cmake_minimum_required(VERSION 3.10)
project(formatter_ex_lib VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Создаем статическую библиотеку formatter_ex
add_library(formatter_ex STATIC ${CMAKE_CURRENT_SOURCE_DIR}/formatter_ex.cpp)

# Указываем директорию с заголовочными файлами
target_include_directories(formatter_ex PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# Линкуем с formatter (теперь просто указываем имя цели, без add_subdirectory)
target_link_libraries(formatter_ex PRIVATE formatter)

# Установка
install(TARGETS formatter_ex
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin)

install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/formatter_ex.h
        DESTINATION include)
