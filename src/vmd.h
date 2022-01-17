#ifndef VMDTOFBX_VMD_H
#define VMDTOFBX_VMD_H
typedef unsigned long DWORD;
typedef unsigned char BYTE;

#include <cstdio>
#include <fstream>
#include <vector>

using namespace std;


struct VMDHeader{
    char Version[30];
    char ModelName[20];
    //unsigned long FrameData[4];
};

struct VMDMotionFrame{
    char BoneName[15];
    DWORD FrameNo;
    float Location[3];
    float Rotation[4];
    BYTE Interpolation[64];
};

//
//
// 表情データ数
struct VMDMorphHeader {
    unsigned long Count; // 表情データ数
} ;

struct VMDMorphFrame {
    char SkinName[15]; // 表情名
    unsigned long FrameNo; // フレーム番号
    float Weight; // 表情の設定値(表情スライダーの値)
};
//
// カメラデータ数
struct VMD_CAMERA_COUNT {
    unsigned long Count; // カメラデータ数
} ;

//// カメラデータ
//struct VMD_CAMERA { // 61 Bytes // カメラ
//    unsigned long FrameNo; // フレーム番号
//    float Length; // -(距離)
//    float Location[3]; // 位置
//    float Rotation[3]; // オイラー角 // X軸は符号が反転しているので注意 // 回転
//    char Interpolation[24]; // おそらく[6][4](未検証) // 補完
//    unsigned long ViewingAngle; // 視界角
//    char Perspective; // 0:on 1:off // パースペクティブ
//} ;
//
//// 照明データ数
//struct VMD_LIGHT_COUNT {
//    unsigned long Count; // 照明データ数
//} ;
//
//// 照明データ
//struct VMD_LIGHT { // 28 Bytes // 照明
//    unsigned long FrameNo; // フレーム番号
//    float RGB[3]; // RGB各値/256 // 赤、緑、青
//    float Location[3]; // X, Y, Z
//} ;
//
//// セルフシャドウデータ数
//struct VMD_SELF_SHADOW_COUNT {
//    unsigned long Count; // セルフシャドウデータ数
//} vmd_self_shadow_count;
//
//// セルフシャドウデータ
//struct VMD_SELF_SHADOW { // 9 Bytes // セルフシャドー
//    unsigned long FrameNo; // フレーム番号
//    char Mode; // 00-02 // モード
//    float Distance; // 0.1 - (dist * 0.00001) // 距離
//};
//
//
class VMD{
public:
    int BoneCount;
    int MorphCount;
    int CameraCount;
//    int LightCount;
//    int ShadowCount;
    VMDHeader Header;
    std::vector<VMDMotionFrame> *MotionFrames;
    std::vector<VMDMorphFrame> *MorphFrames;

public :
    void Read(const char* filePath);
    std::vector<const char*> GetMorphList();

};

#endif //VMDTOFBX_VMD_H
