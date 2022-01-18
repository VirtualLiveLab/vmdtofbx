cmake_minimum_required(VERSION 3.21)
project(vmdtofbx)

set(CMAKE_CXX_STANDARD 14)
set(FBX_SDK_DIR "D:/ProgramFiles/Autodesk/FBX/2020.2.1")
# 64bit
set(CMAKE_C_FLAGS -m64)
set(CMAKE_CXX_FLAGS_DEBUG "/MDd")
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY $<1:${CMAKE_BINARY_DIR}/lib>)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY $<1:${CMAKE_BINARY_DIR}/lib>)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY $<1:${CMAKE_BINARY_DIR}/bin>)

# スクリプトの追加
file(GLOB sources
        ./src/*.cpp
        ./src/*.h
        ./src/Common/*.cxx
        ./src/Common/*.h
        ./src/MyOwnWriterReader/*.cxx
        ./src/MyOwnWriterReader/*.h
        )
add_executable(vmdtofbx ${sources})

# include
include_directories("${FBX_SDK_DIR}/include")


if (WIN32)
    #################
    ## Windows
    #################
    if (CMAKE_BUILD_TYPE STREQUAL "Debug")
        link_directories("${FBX_SDK_DIR}/lib/vs2019/x64/debug")
        file(GLOB libs ${FBX_SDK_DIR}/lib/vs2019/x64/debug/*-md.lib)
        target_link_libraries(${PROJECT_NAME} ${libs} wininet.lib)

        add_custom_command(
                TARGET ${PROJECT_NAME} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy
                ${FBX_SDK_DIR}/lib/vs2019/x64/debug/libfbxsdk.dll
                ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/libfbxsdk.dll)

    else ()
        link_directories("${FBX_SDK_DIR}/lib/vs2019/x64/release")
        file(GLOB libs ${FBX_SDK_DIR}/lib/vs2019/x64/release/*-md.lib)
        target_link_libraries(${PROJECT_NAME} ${libs} wininet.lib)
        add_custom_command(
                TARGET ${PROJECT_NAME} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy
                ${FBX_SDK_DIR}/lib/vs2019/x64/release/libfbxsdk.dll
                ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/libfbxsdk.dll)
    endif ()
else ()
    #################
    ## Linux
    #################
    if (CMAKE_BUILD_TYPE STREQUAL "Debug")
        link_directories("${FBX_SDK_DIR}/lib/gcc/x64/debug")
        file(GLOB libs ${FBX_SDK_DIR}/lib/gcc/x64/debug/*-mdlib.)
        target_link_libraries(${PROJECT_NAME} ${libs})
        add_custom_command(
                TARGET ${PROJECT_NAME} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy
                ${FBX_SDK_DIR}/lib/gcc/x64/debug/libfbxsdk.so
                ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/libfbxsdk.so)
    else ()
        link_directories("${FBX_SDK_DIR}/lib/gcc/x64/release")
        file(GLOB libs ${FBX_SDK_DIR}/lib/gcc/x64/release/*.a)
        target_link_libraries(${PROJECT_NAME} ${libs})
        add_custom_command(
                TARGET ${PROJECT_NAME} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy
                ${FBX_SDK_DIR}/lib/gcc/x64/release/libfbxsdk.so
                ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/libfbxsdk.so)
    endif ()
endif ()





