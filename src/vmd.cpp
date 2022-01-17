#include "vmd.h"

void VMD::Read(const char* filePath) {
    //const char *filename = "F:\\test.vmd";

    // ファイルのOpen
    auto fp = fopen(filePath, "rb");
    //VMDHeader vmdHeader;

    //VMDMotionFrame vmdFrame;
//    int BoneCount;
//    int MorphCount;
//    int CameraCount;
//    int LightCount;
//    int ShadowCount;

    fread(&Header, sizeof(Header), 1, fp);
    fread(&BoneCount, sizeof(int), 1, fp);


    MotionFrames = new std::vector<VMDMotionFrame>(BoneCount);
    for (auto &motion: *MotionFrames) {
        fread(&motion.BoneName, sizeof(motion.BoneName), 1, fp);
        fread(&motion.FrameNo,
              sizeof(motion.FrameNo) +
              sizeof(motion.Location) +
              sizeof(motion.Rotation) +
              sizeof(motion.Interpolation),
              1,
              fp
        );

    }
    fread(&MorphCount, sizeof(int), 1, fp);

    MorphFrames = new std::vector<VMDMorphFrame>(MorphCount);
    for (auto &motion: *MorphFrames) {
        fread(&motion.SkinName, sizeof(motion.SkinName), 1, fp);
        fread(&motion.FrameNo,
              sizeof(motion.FrameNo) +
              sizeof(motion.Weight),
              1,
              fp
        );

//        printf("%s\n", motion.SkinName);
//        printf("%ld\n", motion.FrameNo);
//        printf("%f\n", motion.Weight);
    }

    fread(&CameraCount, sizeof(int), 1, fp);

    // ファイルのClose
    fclose(fp);
}

std::vector<const char*> VMD::GetMorphList(){
    std::vector<const char*> morphList;
    for (auto &item : *MorphFrames) {
        if (item.FrameNo == 0) {
            morphList.push_back(item.SkinName);
        } else {
            break;
        }
    }
    return morphList;
}