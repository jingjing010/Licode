/* 贪心：维护最远可达下标，O(n) */
bool canJump(int* nums, int numsSize) {
    int far = 0;
    for (int i = 0; i < numsSize; i++) {
        if (i > far) return false;
        if (i + nums[i] > far) far = i + nums[i];
        if (far >= numsSize - 1) return true;
    }
    return true;
}
