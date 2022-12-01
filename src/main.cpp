#include <math.h>
#include "vmd.h"
#include <fbxsdk.h>
#include <list>
#include <map>
#include <sstream>
#include "../samples/Common/Common.h"

#define SAMPLE_FILENAME "Test.fbx"
VMD *vmd;

bool CreateScene(FbxScene *pScene, std::map<string, string> setting);

FbxNode *CreateNurbs(FbxScene *pScene, const char *pName);

void MapShapesOnNurbs(FbxScene *pScene, FbxNode *pNurbs,std::map<string, string> settingg);

void AnimateNurbs(FbxNode *pNurbs, FbxScene *pScene, std::map<string, string> setting);
vector<string> convert(vector<const char *> frames, std::map<string, string> maps);

vector<string> split(const string &s, char delim) {
    vector<string> elems;
    stringstream ss(s);
    string item;
    while (getline(ss, item, delim)) {
        if (!item.empty()) {
            elems.push_back(item);
        }
    }
    return elems;
}

int main(int argc, char **argv) {

    const char* filePath = argv[1];

    std::map<string, string> settings;
    for (int i = 2; i < argc; ++i) {
        const char* setStr = argv[i];
        std::vector<string> sets = split(setStr, '=');
        if(sets.size() != 2) exit(0);
        settings[sets[0]] = sets[1];
    }
    //const char *filePath = "F:\\MC2_Miku.vmd";

    vmd = new VMD();
    vmd->Read(filePath);

    FbxManager *lSdkManager = NULL;
    FbxScene *lScene = NULL;
    bool lResult;

    // Prepare the FBX SDK.
    InitializeSdkObjects(lSdkManager, lScene);

    // Create the scene.
    lResult = CreateScene(lScene, settings);

    if (lResult == false) {
        FBXSDK_printf("\n\nAn error occurred while creating the scene...\n");
        DestroySdkObjects(lSdkManager, lResult);
        return 0;
    }

    // Save the scene.

    // The example can take an output file name as an argument.
    const char *lSampleFileName = NULL;
    for (int i = 1; i < argc; ++i) {
        if (FBXSDK_stricmp(argv[i], "-test") == 0) continue;
        else if (!lSampleFileName) lSampleFileName = argv[i];
    }
    if (!lSampleFileName) lSampleFileName = SAMPLE_FILENAME;

    lResult = SaveScene(lSdkManager, lScene, lSampleFileName);
    if (lResult == false) {
        FBXSDK_printf("\n\nAn error occurred while saving the scene...\n");
        DestroySdkObjects(lSdkManager, lResult);
        return 0;
    }

    // Destroy all objects created by the FBX SDK.
    DestroySdkObjects(lSdkManager, lResult);

    return 0;
}

bool CreateScene(FbxScene *pScene, map<string, string> setting) {
    FbxNode *lNurbs = CreateNurbs(pScene, "Face");
    // Build the node tree.
    FbxNode *lRootNode = pScene->GetRootNode();
    lRootNode->AddChild(lNurbs);
    MapShapesOnNurbs(pScene, lNurbs, setting);
    AnimateNurbs(lNurbs, pScene, setting);
    return true;
}

// Create a sphere.
FbxNode *CreateNurbs(FbxScene *pScene, const char *pName) {
    FbxNurbs *lNurbs = FbxNurbs::Create(pScene, pName);

    // Set nurbs properties.
    lNurbs->SetOrder(4, 4);
    lNurbs->SetStep(2, 2);
    lNurbs->InitControlPoints(8, FbxNurbs::ePeriodic, 7, FbxNurbs::eOpen);

    double lUKnotVector[] = {-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0};
    memcpy(lNurbs->GetUKnotVector(), lUKnotVector, lNurbs->GetUKnotCount() * sizeof(double));

    double lVKnotVector[] = {0.0, 0.0, 0.0, 0.0, 1.0, 2.0, 3.0, 4.0, 4.0, 4.0, 4.0};
    memcpy(lNurbs->GetVKnotVector(), lVKnotVector, lNurbs->GetVKnotCount() * sizeof(double));

    FbxVector4 *lVector4 = lNurbs->GetControlPoints();
    int i, j;
    double lScale = 20.0;
    double lPi = 3.14159;
    double lYAngle[] = {90.0, 90.0, 52.0, 0.0, -52.0, -90.0, -90.0};
    double lRadius[] = {0.0, 0.283, 0.872, 1.226, 0.872, 0.283, 0.0};

    for (i = 0; i < 7; i++) {
        for (j = 0; j < 8; j++) {
            double lX = lScale * lRadius[i] * cos(lPi / 4 * j);
            double lY = lScale * sin(2 * lPi / 360 * lYAngle[i]);
            double lZ = lScale * lRadius[i] * sin(lPi / 4 * j);
            double lWeight = 1.0;

            lVector4[8 * i + j].Set(lX, lY, lZ, lWeight);
        }
    }


    FbxNode *lNode = FbxNode::Create(pScene, pName);

    lNode->SetNodeAttribute(lNurbs);

    return lNode;
}

vector<string> convert(vector<const char *> frames, std::map<string, string> maps){
    std::vector<string> convertList;

    for (auto &frame: frames) {
        std::string conv = std::string (frame);

        for (const auto &item: maps) {
            if (frame == item.first) { conv = item.second; }
        }


        convertList.push_back(conv);
    }

    return convertList;
}
// RootNode is bad
void MapShapesOnNurbs(FbxScene *pScene, FbxNode *pNurbs, map<string, string> setting) {

    vector<const char*> list = vmd->GetMorphList();
    auto morphList = convert(list, setting);
    FbxBlendShape *lBlendShape = FbxBlendShape::Create(pScene, "MyBlendShape");
    for (const auto &item: morphList) {
        char *convertItem;
        FbxAnsiToUTF8(item.c_str(), convertItem);

        FbxBlendShapeChannel *channel = FbxBlendShapeChannel::Create(pScene, convertItem);
        FbxFree(convertItem);
        FbxShape *lShape = FbxShape::Create(pScene, item.c_str());
        //lShape->InitControlPoints(8*7);
        channel->AddTargetShape(lShape);
        lBlendShape->AddBlendShapeChannel(channel);
    }
    FbxGeometry *lGeometry = pNurbs->GetGeometry();
    lGeometry->AddDeformer(lBlendShape);
}

// Morph sphere into box shape.
void AnimateNurbs(FbxNode *pNurbs, FbxScene *pScene, std::map<string, string> setting) {
    FbxString lAnimStackName = "MMD Morph";
    FbxTime lTime;

    // First animation stack.
    FbxAnimStack *lAnimStack = FbxAnimStack::Create(pScene, lAnimStackName);

    // The animation nodes can only exist on AnimLayers therefore it is mandatory to
    // add at least one AnimLayer to the AnimStack. And for the purpose of this example,
    // one layer is all we need.
    FbxAnimLayer *lAnimLayer = FbxAnimLayer::Create(pScene, "Base Layer");
    lAnimStack->AddMember(lAnimLayer);

    FbxGeometry *lNurbsAttribute = (FbxGeometry *) pNurbs->GetNodeAttribute();

    // The stretched shape is at index 0 because it was added first to the nurbs.
    //FbxAnimCurve* lCurve = lNurbsAttribute->GetShapeChannel(0, 0, lAnimLayer, true);

    vector<const char*> list = vmd->GetMorphList();
    auto morphList = convert(list, setting);
    int i = 0;
    for (const auto &morph: morphList){
        auto lCurve = lNurbsAttribute->GetShapeChannel(0, i, lAnimLayer, true);
        if (lCurve) {
            lCurve->KeyModifyBegin();
            for (const auto frame: *vmd->MorphFrames) {

                std::string name = std::string(frame.SkinName);
                for (const auto &item: setting)
                    if (std::string(frame.SkinName) == item.first) name = item.second;

                if (name == std::string(morph)) {
                    printf("%ld %s\n", frame.FrameNo, morph.c_str());
                    lTime.SetFrame(frame.FrameNo);
                    auto index = lCurve->KeyAdd(lTime);
                    //lCurve->KeySetValue(i, frame.Weight);
                    lCurve->KeySet(index, lTime, frame.Weight * 100.0, FbxAnimCurveDef::eInterpolationLinear);
                    //lCurve->KeySetInterpolation(i, FbxAnimCurveDef::eInterpolationCubic);

                }
            }
            lCurve->KeyModifyEnd();
        }
        i++;
    }
}


