cmake_minimum_required(VERSION 3.14)
project(lab05)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Принудительно используем /MT на Windows для всех целей
if(MSVC)
    set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} /MT")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} /MTd")
    set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} /MT")
    set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} /MTd")
endif()

# Основная библиотека print
add_library(print STATIC sources/print.cpp)
target_include_directories(print PUBLIC include)

# Библиотека banking
add_subdirectory(banking_lib)

# Опции для тестов
option(BUILD_TESTS "Build tests for print" OFF)
option(BUILD_BANKING_TESTS "Build tests for banking" OFF)

# Тесты для print
if(BUILD_TESTS)
    enable_testing()
    
    include(FetchContent)
    FetchContent_Declare(
        googletest
        GIT_REPOSITORY https://github.com/google/googletest.git
        GIT_TAG v1.15.2
    )
    
    # Отключаем предупреждения и настраиваем gtest для использования /MT
    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
    FetchContent_MakeAvailable(googletest)
    
    file(GLOB TEST_SOURCES "tests/*.cpp")
    add_executable(check ${TEST_SOURCES})
    target_link_libraries(check print gtest_main)
    add_test(NAME check COMMAND check)
endif()

include(CPackConfig.cmake)
