cmake_minimum_required(VERSION 3.17)
project(vmdtofbx)

# FBX SDK のパスを指定 - ビルド前に変更してください
set(FBX_SDK_ROOT "C:/Program Files/Autodesk/FBX/FBX SDK/2020.3.7")

# OS の確認
if(NOT WIN32 AND NOT UNIX)
    message(FATAL_ERROR "Only Windows (MSVC) or UNIX is supported.")
endif()

# Windows のみの FbxAnsiToUTF8() への代替
if(UNIX)
    find_package(Iconv REQUIRED)
endif()

# CMAKE_CXX_FLAGS ではなく Abstraction によって MSVC runtime library を指定
if(POLICY CMP0091)
    cmake_policy(SET CMP0091 NEW)
endif(POLICY CMP0091)

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
if(WIN32)
    target_compile_options(${PROJECT_NAME} PRIVATE /source-charset:UTF-8)
elseif(UNIX)
    target_compile_options(${PROJECT_NAME} PRIVATE -finput-charset=UTF-8)
endif()

# FBX SDK には libfbxsdk の pdb ファイルが含まれていない（同ウェブサイトで別途配布）
# そのため、Debug ビルドの際の LNK4099 エラーは出力されないようにしておく
if(WIN32)
    target_link_options(${PROJECT_NAME} PRIVATE /IGNORE:4099)
endif()

# ライブラリのリンク
if(WIN32)
    if(FBX_SHARED)
        target_link_libraries(${PROJECT_NAME} PRIVATE fbxsdk)
    else()
        # 公式ドキュメント「Configuring the FBX SDK for Windows」の Configuring Visual Studio を参照
        target_link_options(${PROJECT_NAME} PRIVATE $<$<CONFIG:Debug>:/NODEFAULTLIB:LIBCMT>)
        target_link_libraries(${PROJECT_NAME} PRIVATE fbxsdk $<$<CONFIG:Debug>:wininet.lib>)
    endif()
elseif(UNIX)
    target_link_libraries(${PROJECT_NAME} PRIVATE fbxsdk Iconv::Iconv)
endif()

# ライブラリリンク後の設定（fbxsdk.cmakeで定義された関数）
fbx_target_finalize(${PROJECT_NAME})