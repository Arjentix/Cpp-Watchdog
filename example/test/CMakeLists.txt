cmake_minimum_required(VERSION 3.0.0)

include(CTest)
enable_testing()

set(THIS foo_test)

set(SOURCE
  foo_test.cpp
)

add_executable(${THIS} ${SOURCE})

set_target_properties(${THIS} PROPERTIES
  CXX_STANDARD 17
  CXX_STANDARD_REQUIRED ON
  CMAKE_CXX_EXTENSIONS OFF
)

target_include_directories(${THIS} PRIVATE
    ${PROJECT_SOURCE_DIR}/src
)

target_link_libraries(${THIS} PRIVATE
    gtest_main
    foo
)

add_test(
    NAME ${THIS}
    COMMAND ${THIS}
)
