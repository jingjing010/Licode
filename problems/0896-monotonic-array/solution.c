/* 一遍扫描，记录是否出现过上升 / 下降，O(n) */
bool isMonotonic(int* nums, int numsSize) {
    bool up = false, down = false;
    for (int i = 1; i < numsSize; i++) {
        if (nums[i] > nums[i - 1]) up = true;
        if (nums[i] < nums[i - 1]) down = true;
        if (up && down) return false;
    }
    return true;
}
