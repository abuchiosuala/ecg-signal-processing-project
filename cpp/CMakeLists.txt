cmake_minimum_required(VERSION 3.29)
project(ecg_signal_processing_project)

set(CMAKE_CXX_STANDARD 17)

add_executable(ecg_signal_processing_project
        ${CMAKE_SOURCE_DIR} main.cpp
        ${CMAKE_SOURCE_DIR} loadData.cpp)
