# vmdtofbx

現在VMDに含まれる表情データのみを球体に張り付けてFbxにすることが可能
自分でBuildするためには、FbxSDKの設定が必要なので注意してください

作者はUnityでfbxを取り込んでAnimationを取りこんでます。不具合が
BugとかあったらIssueくれたらうれしいです

## Environment

- cmake 3.16 or higher
- Visual Studio 16 2019
- FBXSDK 2020.2.1

## How to build

### windows

1. cmakeファイルの編集 

    導入したFBXSDKのパスに合わせて
    5行目のファイルパスを変えてください
    ```asm
    set(FBX_SDK_DIR "D:/ProgramFiles/Autodesk/FBX/2020.2.1")
    ```
2. ビルド方法

    以下のコマンドでプロジェクトの作成を行ってください
    ```asm
    mkdir build
    cd build
    cmake ..
    cmake --build .
    ```

    Debug Buildの場合はこちらのオプションをつけて実行してください
    ```asm
    cmake .. -DCMAKE_BUILD_TYPE=Debug
    ```

    VisualStudioのプロジェクトが作成されるので、ReleaseもしくはDebugモードでビルドを行ってください.

---
### linux
開発中です

## How to use

Releaseからexeを落としてきてパスを通してください。

以下のコマンドを打つことで実行できます
```
vmdtofbx <vmdファイルのパス>
```

License
-------

[MIT](LICENSE.md)ですがコメントくれたら作者は喜びます(*'ω'*)
