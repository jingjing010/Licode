/* 排序 + 固定一个数 + 双指针，O(n^2) */
static int cmpInt3(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    return (x > y) - (x < y);
}

int** threeSum(int* nums, int numsSize, int* returnSize, int** returnColumnSizes) {
    qsort(nums, numsSize, sizeof(int), cmpInt3);
    int cap = 16, cnt = 0;
    int** res = (int**)malloc(sizeof(int*) * cap);
    int* cols = (int*)malloc(sizeof(int) * cap);
    for (int i = 0; i < numsSize - 2; i++) {
        if (nums[i] > 0) break;
        if (i > 0 && nums[i] == nums[i - 1]) continue;
        int l = i + 1, r = numsSize - 1;
        while (l < r) {
            int sum = nums[i] + nums[l] + nums[r];
            if (sum < 0) {
                l++;
            } else if (sum > 0) {
                r--;
            } else {
                if (cnt == cap) {
                    cap *= 2;
                    res = (int**)realloc(res, sizeof(int*) * cap);
                    cols = (int*)realloc(cols, sizeof(int) * cap);
                }
                res[cnt] = (int*)malloc(sizeof(int) * 3);
                res[cnt][0] = nums[i];
                res[cnt][1] = nums[l];
                res[cnt][2] = nums[r];
                cols[cnt++] = 3;
                while (l < r && nums[l] == nums[l + 1]) l++;
                while (l < r && nums[r] == nums[r - 1]) r--;
                l++;
                r--;
            }
        }
    }
    *returnSize = cnt;
    *returnColumnSizes = cols;
    return res;
}
