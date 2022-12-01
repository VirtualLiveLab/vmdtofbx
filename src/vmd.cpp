#include "vmd.h"

void VMD::Read(const char *filePath) {
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
    for (auto &morph: *MorphFrames) {
        fread(&morph.SkinName, sizeof(morph.SkinName), 1, fp);
        fread(&morph.FrameNo,
              sizeof(morph.FrameNo) +
              sizeof(morph.Weight),
              1,
              fp
        );

//        printf("%s\n", morph.SkinName);
//        printf("%ld\n", morph.FrameNo);
//        printf("%f\n", morph.Weight);
    }


    fread(&CameraCount, sizeof(int), 1, fp);

    // ファイルのClose
    fclose(fp);
}


bool contains(std::vector<const char *> &listOfElements, const char *element) {
    for (const auto &item: listOfElements)
        if (std::string(item) == std::string(element))
            return true;


    return false;
}


std::vector<const char *> VMD::GetMorphList() {
    std::vector<const char *> morphList;
    for (auto &morph: *MorphFrames)
        if (!contains(morphList, morph.SkinName))
            morphList.push_back(morph.SkinName);

    return morphList;
}
