/* 荷兰国旗：三指针一趟扫描，O(n) 时间 O(1) 空间 */
void sortColors(int* nums, int numsSize) {
    int p0 = 0, i = 0, p2 = numsSize - 1;
    while (i <= p2) {
        if (nums[i] == 0) {
            int t = nums[i]; nums[i] = nums[p0]; nums[p0] = t;
            p0++;
            i++;
        } else if (nums[i] == 2) {
            int t = nums[i]; nums[i] = nums[p2]; nums[p2] = t;
            p2--;
        } else {
            i++;
        }
    }
}
