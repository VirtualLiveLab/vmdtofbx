#include <string>
#include <vector>

#ifdef _WIN32
#include <fbxsdk.h>
#include <Windows.h>
#else
#include <iconv.h>
#endif

#ifdef _WIN32

bool IsShiftJISEnvironment()
{
    return GetConsoleCP() == 932; // 932 = Shift_JIS
}

std::string sjis_to_utf8(const std::string &input)
{
    std::string name_converted;
    char *utf8Str = nullptr;
    size_t utf8Size = 0;

    FbxAnsiToUTF8(input.c_str(), utf8Str, &utf8Size);
    if (utf8Str)
    {
        name_converted = std::string(utf8Str);
        FbxFree(utf8Str);
    }
    return name_converted;
}

#else

bool IsShiftJISEnvironment()
{
    return false;
}

std::string sjis_to_utf8(const std::string &input)
{
    iconv_t cd = iconv_open("UTF-8", "SHIFT_JIS");
    if (cd == (iconv_t)-1)
    {
        perror("iconv_open failed");
        return "";
    }

    size_t inSize = input.size();
    size_t outSize = inSize * 4;
    char *inBuf = const_cast<char *>(input.c_str());
    std::vector<char> outBuf(outSize);
    char *outPtr = outBuf.data();

    if (iconv(cd, &inBuf, &inSize, &outPtr, &outSize) == (size_t)-1)
    {
        perror("iconv failed");
        iconv_close(cd);
        return "";
    }

    iconv_close(cd);
    return std::string(outBuf.data());
}

#endif