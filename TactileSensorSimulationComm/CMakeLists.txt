cmake_minimum_required(VERSION 3.17)
project(TactileSensorSimulationComm)

set(CMAKE_CXX_STANDARD 14)

add_library(TactileSensorSimulationComm SHARED comm.cpp comm.h)
target_link_libraries(TactileSensorSimulationComm util)

add_executable(libTest test.cpp)
target_link_libraries(libTest TactileSensorSimulationComm)