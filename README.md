# vmdtofbx
vmdファイルに含まれる表情データのみを面のメッシュに記録し、fbx形式にして出力するプロジェクト

<br>

## 環境
- cmake 3.17 and above

- FBX SDK 2020.3.7

- Windows の場合
    - Visual Studio 17 2022

- Linux の場合
    - GCC version 9.3 and above
    - iconv

<br>

## ビルド方法

### Windows

1. CMakeLists.txt の編集 

    導入した FBX SDK のパスに合わせて `FBX_SDK_ROOT` の設定パスを変えてください。
    ```CMake
    set(FBX_SDK_ROOT "C:/Program Files/Autodesk/FBX/FBX SDK/2020.3.7")
    ```

2. ビルド

    - 動的リンクの場合

        ```Bash
        cd src
        cmake -S . -B build -DFBX_SHARED=1
        cmake --build build --config <config> # Release または Debug
        ```

    - 静的リンクの場合

        ```Bash
        cd src
        cmake -S . -B build -DFBX_STATIC_RTL=1
        cmake --build build --config <config> # Release または Debug
        ```

    いずれも *build/\<config>* 下にビルドされたファイルが出力されます。<br>
    動的リンクの場合、同ディレクトリに libfbxsdk.dll がコピーされます。


### Linux

```Bash
cd src
cmake -S . B build -DCMAKE_BUILD_TYPE=<config> # Release または Debug
cmake --build build
```

*build* 下にビルドされたファイルが生成され、*build/\<config>* 下に libfbxsdk.so がコピーされます。



<br>

## 使用方法
まず vmdファイルを引数にとり、その後「"変換したい名前=変換後の名前"」という形式でシェイプキー名の変換を指定してください。

```
path/to/vmdtofbx path/to/<filename>.vmd "あ=a" "い=i" "う=u" "え=e" "お=o"
```

vmdファイルと同じディレクトリに「<vmdファイルの名前>.fbx」が生成されます。

<br>

License
-------

[MIT](LICENSE.md)ですがコメントくれたら作者は喜びます(*'ω'*)