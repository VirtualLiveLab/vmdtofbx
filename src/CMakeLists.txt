cmake_minimum_required(VERSION 3.17)
project(vmdtofbx)

# FBX SDK のパスを指定 - ビルド前に変更してください
if(WIN32 AND MSVC)
    set(FBX_SDK_ROOT "C:/Program Files/Autodesk/FBX/FBX SDK/2020.3.7")
elseif(UNIX)
    set(FBX_SDK_ROOT "/home/username/fbxsdk")
    # Windows のみの FbxAnsiToUTF8() への代替
    find_package(Iconv REQUIRED)
else()
    message(FATAL_ERROR "Only Windows (MSVC) or UNIX is supported.")
endif()

# アーキテクチャの種類を取得
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
    if("${CMAKE_C_COMPILER_ARCHITECTURE_ID}" STREQUAL "ARM64")
        SET(FBX_ARM 1)
        set(FBX_ARCH arm64)
    else()
        set(FBX_ARCH x64)
    endif()
endif()

# fbxsdk.cmake で使用される変数の設定と、そのサンプルスクリプトの実行
set(FBX_BUILD_ROOT ${CMAKE_BINARY_DIR})
include("${FBX_SDK_ROOT}/samples/fbxsdk.cmake")

# Dynamic Link の場合の Processer Definition の設定
if(FBX_SHARED)
    add_compile_definitions(FBXSDK_SHARED)
endif()

# プロジェクトのソースを追加
add_executable(${PROJECT_NAME}
    main.cpp
    ConvertEncoding.h
    FbxShapeUtils.h
    vmd.h
)

# コンパイルオプションの設定
if(MSVC)
    target_compile_options(${PROJECT_NAME} PRIVATE /source-charset:UTF-8)
elseif(UNIX)
    target_compile_options(${PROJECT_NAME} PRIVATE -finput-charset=UTF-8)
endif()

# Note:
#    "debug" ディレクトリ下のライブラリが何故かデバッグ情報持っていないらしい
#   今は警告を非表示にしています
if(WIN32)
    target_link_options(${PROJECT_NAME} PRIVATE /IGNORE:4099)
endif()

# ライブラリのリンク
if(FBX_STATIC_MT OR FBX_STATIC_MD)
    target_link_options(${PROJECT_NAME} PRIVATE $<$<CONFIG:Debug>:/NODEFAULTLIB:LIBCMT>)
    target_link_libraries(${PROJECT_NAME} PRIVATE fbxsdk $<$<CONFIG:Debug>:wininet.lib>)
elseif(UNIX)
    target_link_libraries(${PROJECT_NAME} PRIVATE fbxsdk Iconv::Iconv)
else()
    target_link_libraries(${PROJECT_NAME} PRIVATE fbxsdk)
endif()

# ライブラリリンク後の設定（サンプルスクリプトで定義）
fbx_target_finalize(${PROJECT_NAME})