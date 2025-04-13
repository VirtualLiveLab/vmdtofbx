// VMD format & functions
// source : https://blog.goo.ne.jp/torisu_tetosuki/e/bc9f1c4d597341b394bd02b64597499d

#ifndef __VMD_H__
#define __VMD_H__

#include <cstdint>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>

#pragma pack(push, 1)

static const size_t VMD_HEADER_SIZE = 50;
static const size_t VMD_MOTION_SIZE = 111;

// 表情データ
struct VMD_SKIN
{
    char SkinName[15]; // Shift_JIS
    uint32_t FrameNo;
    float Weight;
};

// vmdファイル内の表情データ部分の読み出し
std::vector<VMD_SKIN> ReadAndGetSkinData(std::ifstream &vmdfile)
{
    // skin count 部分まで読み飛ばす
    vmdfile.ignore(VMD_HEADER_SIZE);
    uint32_t vmd_motion_count;
    vmdfile.read(reinterpret_cast<char *>(&vmd_motion_count), sizeof(vmd_motion_count));
    for (size_t i = 0; i < static_cast<size_t>(vmd_motion_count); i++)
    {
        vmdfile.ignore(VMD_MOTION_SIZE);
    }

    // skin count 部分の読み出し
    uint32_t vmd_skin_count;
    vmdfile.read(reinterpret_cast<char *>(&vmd_skin_count), sizeof(vmd_skin_count));

    // skin data の取得
    std::vector<VMD_SKIN> skindata;
    for (size_t i = 0; i < static_cast<size_t>(vmd_skin_count); i++)
    {
        VMD_SKIN vmd_skin;
        vmdfile.read(reinterpret_cast<char *>(&vmd_skin), sizeof(VMD_SKIN));
        skindata.push_back(vmd_skin);
    }
    return skindata;
}

// 取得した vmdの表情の全データより、シェイプキー一覧の抽出
std::vector<std::string> GetShapekeyNames(std::vector<VMD_SKIN> pSkinData)
{
    std::vector<std::string> shapekey_names;
    for (const auto &skin : pSkinData)
    {
        std::string shapekey_name(skin.SkinName);
        auto it = std::find(shapekey_names.begin(), shapekey_names.end(), shapekey_name);
        if (it == shapekey_names.end())
        {
            shapekey_names.push_back(shapekey_name);
        }
    }
    return shapekey_names;
}

#pragma pack(pop)

#endif //__VMD_H__