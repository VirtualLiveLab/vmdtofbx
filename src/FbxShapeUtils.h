#include <fbxsdk.h>
#include <vector>
#include <string>
#include <unordered_map>

// シェイプアニメーション記録用の四角いメッシュを作成
FbxMesh *CreateSquareMesh(FbxScene *pScene)
{
    FbxMesh *lMesh = FbxMesh::Create(pScene, "VMDshapeAnimation");

    // 四角いメッシュの4つの頂点を定める
    FbxVector4 vertices[4] = {
        {-50, -50, 0}, // Bottom left
        {50, -50, 0},  // Bottom right
        {50, 50, 0},   // Top right
        {-50, 50, 0}   // Top left
    };

    // メッシュに頂点（Control Point）を登録
    lMesh->InitControlPoints(4);
    for (int i = 0; i < 4; i++)
    {
        lMesh->SetControlPointAt(vertices[i], i);
    }

    // 登録した Control Point からポリゴンを構成
    lMesh->BeginPolygon();
    for (int i = 0; i < 4; i++)
    {
        lMesh->AddPolygon(i);
    }
    lMesh->EndPolygon();

    return lMesh;
}

// メッシュ内のシェイプキー関連要素を設定
void ConfigureBlendShapeDeformer(FbxMesh *pMesh, FbxAnimLayer *pAnimlayer, std::vector<std::string> pShapekeyNames)
{
    // BlendShapeDeformer を作成
    FbxBlendShape *lBlendShapeDeformer = FbxBlendShape::Create(pMesh, "Deformer_VMDshapeAnimation");
    pMesh->AddDeformer(lBlendShapeDeformer);

    for (int i = 0; i < pShapekeyNames.size(); i++)
    {
        const char *shapekey_name = pShapekeyNames.at(i).c_str();

        // BlendShapeChannel を作成
        FbxBlendShapeChannel *lBlendShapeChannel = FbxBlendShapeChannel::Create(lBlendShapeDeformer, shapekey_name);
        lBlendShapeDeformer->AddBlendShapeChannel(lBlendShapeChannel);

        // Shape を作成し、BlendShapeChannel に登録
        FbxShape *targetshape = FbxShape::Create(pMesh, shapekey_name);
        lBlendShapeChannel->AddTargetShape(targetshape);
    }
}

// メッシュ内のシェイプキーの AnimationCurve を作成し、シェイプキー名とのマップを返す
std::unordered_map<std::string, FbxAnimCurve *> CreateShapeCurveMap(FbxMesh *pMesh, FbxAnimLayer *pAnimLayer)
{
    std::unordered_map<std::string, FbxAnimCurve *> shapecurvemap;

    FbxBlendShape *lBlendShapeDeformer = FbxCast<FbxBlendShape>(pMesh->GetDeformer(0));
    for (int i = 0; i < lBlendShapeDeformer->GetBlendShapeChannelCount(); i++)
    {
        FbxBlendShapeChannel *shapekey = lBlendShapeDeformer->GetBlendShapeChannel(i);

        // AnimationCurveNode と AnimationCurve を作成
        FbxAnimCurveNode *lAnimCurveNode = shapekey->DeformPercent.GetCurveNode(pAnimLayer, true);
        shapecurvemap.emplace(shapekey->GetName(), shapekey->DeformPercent.GetCurve(pAnimLayer, true));
    }

    return shapecurvemap;
}

// 既存のシェイプキーの名称を変更
void UpdateShapekeyName(FbxMesh *pMesh, std::string pOldName, std::string pNewName)
{
    FbxBlendShape *lBlendShapeDeformer = FbxCast<FbxBlendShape>(pMesh->GetDeformer(0));
    for (int i = 0; i < lBlendShapeDeformer->GetBlendShapeChannelCount(); i++)
    {
        FbxBlendShapeChannel *shapekey = lBlendShapeDeformer->GetBlendShapeChannel(i);
        if (std::string(shapekey->GetName()) == pOldName)
        {
            // BlendShapeChannel と Shape の両方の名称を変える
            shapekey->SetName(pNewName.c_str());
            shapekey->GetTargetShape(0)->SetName(pNewName.c_str());
        }
    }
}