int missingNumber(int* nums, int numsSize) {
    int x = numsSize;
    for (int i = 0; i < numsSize; i++) x ^= i ^ nums[i];
    return x;
}
