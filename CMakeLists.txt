cmake_minimum_required(VERSION 3.10)
project(Labellisation VERSION 1.0 LANGUAGES CXX)

# Standard C++17
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Optimisation flags
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -march=native")
set(CMAKE_CXX_FLAGS_DEBUG "-g -Wall -Wextra -Wpedantic")

# Définir les répertoires d'include
include_directories(${PROJECT_SOURCE_DIR}/src)

# Collecter tous les fichiers source
file(GLOB_RECURSE CORE_SOURCES "src/core/*.cpp")
file(GLOB_RECURSE IO_SOURCES "src/io/*.cpp")
file(GLOB_RECURSE ALGO_SOURCES "src/algorithms/*.cpp")
file(GLOB_RECURSE UTILS_SOURCES "src/utils/*.cpp")

# Bibliothèque commune avec tous les modules
add_library(labellisation_lib
    ${CORE_SOURCES}
    ${IO_SOURCES}
    ${ALGO_SOURCES}
    ${UTILS_SOURCES}
)

# Exécutable principal
add_executable(labellisation src/main.cpp)
target_link_libraries(labellisation labellisation_lib)

# Tests unitaires
file(GLOB TEST_SOURCES "tests/*.cpp")
foreach(test_source ${TEST_SOURCES})
    get_filename_component(test_name ${test_source} NAME_WE)
    add_executable(${test_name} ${test_source})
    target_link_libraries(${test_name} labellisation_lib)
endforeach()

# Benchmark
file(GLOB BENCHMARK_SOURCES "benchmarks/*.cpp")
foreach(benchmark_source ${BENCHMARK_SOURCES})
    get_filename_component(benchmark_name ${benchmark_source} NAME_WE)
    add_executable(${benchmark_name} ${benchmark_source})
    target_link_libraries(${benchmark_name} labellisation_lib)
endforeach()

# Installation
install(TARGETS labellisation DESTINATION bin)
