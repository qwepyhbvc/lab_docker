cmake_minimum_required(VERSION 3.10)
project(solver_app VERSION 1.0.0)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(equation ${CMAKE_CURRENT_SOURCE_DIR}/equation.cpp)
target_link_libraries(equation PRIVATE formatter_ex solver)

install(TARGETS equation
        RUNTIME DESTINATION bin)
