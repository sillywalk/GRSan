#include <cstdint>
#include <cstdio>

extern "C" int fuzzthing(const uint8_t *Data, size_t Size) {
    if (Size == 15) {
        printf("Jackpot\n");
    } else {
        printf("You didn't find the jackpot... Try again\n");
    }
    return 0;
}

extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    printf("%ld is size\n", Size);
    int success = fuzzthing(Data, Size);
    printf("%d is size\n", success);
    return 0;  // Non-zero return values are reserved for future use.
}
