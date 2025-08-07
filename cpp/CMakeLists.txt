cmake_minimum_required(VERSION 3.10)
project(ssr_simulator LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(target_compile_options_flag "-O3;-march=native")

set(INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include)

add_executable(${PROJECT_NAME}
    main.cpp src/ssr.cpp 
)
target_include_directories(${PROJECT_NAME} PRIVATE ${INCLUDE_DIR})
target_compile_options(${PROJECT_NAME} PRIVATE ${target_compile_options_flag})