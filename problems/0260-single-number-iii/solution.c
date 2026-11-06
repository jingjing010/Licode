int* singleNumber(int* nums, int numsSize, int* returnSize) {
    unsigned int x = 0;
    for (int i = 0; i < numsSize; i++) x ^= (unsigned int)nums[i];
    unsigned int low = x & (0u - x);
    int a = 0, b = 0;
    for (int i = 0; i < numsSize; i++) {
        if ((unsigned int)nums[i] & low) a ^= nums[i];
        else b ^= nums[i];
    }
    int* res = (int*)malloc(sizeof(int) * 2);
    res[0] = a;
    res[1] = b;
    *returnSize = 2;
    return res;
}
