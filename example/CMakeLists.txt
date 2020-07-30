cmake_minimum_required(VERSION 3.0.0)
project(foo VERSION 0.1.0)

include(CTest)
enable_testing()

set(THIS foo)

set(SOURCE
  src/foo.cpp
)

set(BUILD_FLAGS "-Wall -Wextra -pedantic -Werror")

if(CMAKE_BUILD_TYPE MATCHES Debug)
  set(BIN_DIR "${PROJECT_SOURCE_DIR}/bin/debug")
elseif(CMAKE_BUILD_TYPE MATCHES Release)  
  set(BIN_DIR "${PROJECT_SOURCE_DIR}/bin/release")
endif()

add_library(${THIS} ${SOURCE})

set_target_properties(${THIS} PROPERTIES
  CXX_STANDARD 17
  CXX_STANDARD_REQUIRED ON
  CMAKE_CXX_EXTENSIONS OFF
  RUNTIME_OUTPUT_DIRECTORY ${BIN_DIR}
  COMPILE_FLAGS ${BUILD_FLAGS}
)

# If it's not a sub-project
if (CMAKE_SOURCE_DIR STREQUAL PROJECT_SOURCE_DIR)
    add_subdirectory(external/google)
    add_subdirectory(test)
endif()

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
