int dominantIndex(int *nums, int numsSize) {
    int index = 0;
    for (int i = 1; i < numsSize; ++i)
        if (nums[i] > nums[index])
            index = i;
    for (int i = 0; i < numsSize; ++i)
        if (i != index && nums[index] < 2 * nums[i])
            return -1;
    return index;
}
