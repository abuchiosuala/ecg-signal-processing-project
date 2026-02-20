cmake_minimum_required(VERSION 3.29)
project(ecg_signal_processing_project)

set(CMAKE_CXX_STANDARD 14)

add_executable(ecg_signal_processing_project
    src/main.cpp src/loadData.cpp)
