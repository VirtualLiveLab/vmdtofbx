#include <iostream>
#include <filesystem>
#include "vmd.h"
#include "FbxShapeUtils.h"
#include "ConvertEncoding.h"
using namespace std;

// 変換状況をデバッグ表示する関数
void DebugConverting(uint32_t frame_no, string name_processing, unordered_map<string, string> shape_rename_map);

int main(int argc, char *argv[])
{
    // vmdファイルの読み込み
    filesystem::path vmdfilepath(argv[1]);
    if (!filesystem::exists(vmdfilepath))
    {
        cerr << "Error : Cannot find the vmd file. -> " << vmdfilepath.string() << endl;
        return -1;
    }
    ifstream vmdfile(vmdfilepath, ios::binary);

    // vmdファイルから、表情アニメーション全フレームと、シェイプキーの一覧を取得
    vector<VMD_SKIN> skindata = ReadAndGetSkinData(vmdfile);
    vector<string> shapekey_names = GetShapekeyNames(skindata);

    // FBX SDK では UTF-8 で扱う必要あり
    for (auto &name : shapekey_names)
    {
        name = sjis_to_utf8(name);
    }

    // 引数を用いて、シェイプキー名称の変更前後のマップを作成
    unordered_map<string, string> shape_rename_map;
    for (int i = 2; i < argc; ++i)
    {
        string arg(argv[i]);
        size_t pos = arg.find('=');
        if (pos != string::npos)
        {
            string key = arg.substr(0, pos);
            string value = arg.substr(pos + 1);
            shape_rename_map[key] = value;
        }
    }

    // FbxManager, FbxIOSettings の設定と新規Scene の作成
    FbxManager *lSdkManager = FbxManager::Create();
    FbxIOSettings *IOSettings = FbxIOSettings::Create(lSdkManager, IOSROOT);
    lSdkManager->SetIOSettings(IOSettings);
    FbxScene *lScene = FbxScene::Create(lSdkManager, "New Scene");

    // 出力先パスの設定と、Exporter の準備
    string fbxfilename = vmdfilepath.stem().string() + ".fbx";
    filesystem::path outputfbxpath = vmdfilepath.parent_path() / fbxfilename;
    FbxExporter *lExporter = FbxExporter::Create(lSdkManager, "");

    // Initialize() に渡す出力パスが Shift-JIS だった場合、Initialize() は true を返すが Export時にエラーが起きる
    string outputfbxpathStr = IsShiftJISEnvironment() ? sjis_to_utf8(outputfbxpath.string()) : outputfbxpath.string();

    bool exporter_prepared = lExporter->Initialize(outputfbxpathStr.c_str(), -1, IOSettings);

    if (exporter_prepared)
        cout << "The exporter successfully initialized." << endl;
    else
    {
        cerr << "Initializing the exporter failed..." << endl;
        vmdfile.close();
        lSdkManager->Destroy();
        return -1;
    }

    // FbxAnimStack と FbxAnimationLayer の作成
    FbxAnimStack *lAnimStack = FbxAnimStack::Create(lScene, "Take_VMDshapeAnimation");
    FbxAnimLayer *lAnimLayer = FbxAnimLayer::Create(lScene, "BaseAnimation");
    lAnimStack->AddMember(lAnimLayer);

    // アニメーションを記録するメッシュの作成
    FbxMesh *lMesh = CreateSquareMesh(lScene);
    FbxNode *lMeshNode = FbxNode::Create(lScene, "VMDshapeAnimation");
    lMeshNode->SetNodeAttribute(lMesh);
    lScene->GetRootNode()->AddChild(lMeshNode);

    // メッシュにシェイプキーを作成
    ConfigureBlendShapeDeformer(lMesh, shapekey_names);

    // シェイプキーの AnimationCurve を設定し、シェイプキー名とのマップを作成
    unordered_map<string, FbxAnimCurve *> shapecurvemap = CreateShapeCurveMap(lMesh, lAnimLayer);

    // フレーム毎にシェイプキーに対応する AnimationCurve を取得してアニメーションを記録
    for (const auto &frame : skindata)
    {
        string shapekey_name = sjis_to_utf8(string(frame.SkinName));
        auto it = shapecurvemap.find(shapekey_name);
        if (it != shapecurvemap.end())
        {
            FbxAnimCurve *lCurve = it->second;
            if (lCurve)
            {
                lCurve->KeyModifyBegin();

                // 表情の1フレーム分のキーを登録
                FbxTime lTime;
                lTime.SetFrame(frame.FrameNo, FbxTime::eFrames30); // MMD は 30fps
                int keyindex = lCurve->KeyAdd(lTime);

                // MMDでのシェイプキー値は 0~1 なので、fbxに合わせて100倍する
                lCurve->KeySet(keyindex, lTime, frame.Weight * 100.0, FbxAnimCurveDef::eInterpolationLinear);

                lCurve->KeyModifyEnd();

                // ターミナルに変換状況をデバッグ表示
                DebugConverting(frame.FrameNo, frame.SkinName, shape_rename_map);
            }
        }
    }

    // 名称変更前後のマップ（引数の指定から作成）を元に、既存のシェイプキー名を変更
    for (const auto &map : shape_rename_map)
    {
        std::string name_old = IsShiftJISEnvironment() ? sjis_to_utf8(map.first) : map.first;
        std::string name_new = map.second;
        UpdateShapekeyName(lMesh, name_old, name_new);
    }

    // Scene の出力
    if (lExporter->Export(lScene))
        cout << "\nProgram Success!" << endl;
    else
    {
        cout << "\nError occurred while exporting the scene..." << endl;
        cout << lExporter->GetStatus().GetErrorString() << endl;
    }

    // Cleanup
    vmdfile.close();
    lSdkManager->Destroy();

    return 0;
}

void DebugConverting(uint32_t frame_no, string name_processing, unordered_map<string, string> shape_rename_map)
{
    string key = IsShiftJISEnvironment() ? name_processing : sjis_to_utf8(name_processing);

    unordered_map<string, string>::const_iterator it = shape_rename_map.find(key);
    if (it != shape_rename_map.end())
    {
        cout << frame_no << " " << key << " -> " << it->second << endl;
    }
}