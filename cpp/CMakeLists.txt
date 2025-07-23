cmake_minimum_required(VERSION 3.10)
project(ssr_simulator)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(main.x main.cpp src/ssr.cpp)

target_include_directories(main.x PRIVATE include)

target_compile_options(main.x PRIVATE -O3 -march=native)
