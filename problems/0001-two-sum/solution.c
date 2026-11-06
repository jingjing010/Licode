/* 哈希表（开放寻址法）解法，O(n) */
#define HASH_SIZE 32768 /* 2 的幂，且大于 2 * 10^4 */

int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    static long long keys[HASH_SIZE];
    static int vals[HASH_SIZE];
    static bool used[HASH_SIZE];
    memset(used, 0, sizeof(used));

    int* res = (int*)malloc(sizeof(int) * 2);
    *returnSize = 2;
    for (int i = 0; i < numsSize; i++) {
        long long need = (long long)target - nums[i];
        /* 查找 need */
        unsigned int h = (unsigned int)(need * 2654435761LL) & (HASH_SIZE - 1);
        while (used[h]) {
            if (keys[h] == need) {
                res[0] = vals[h];
                res[1] = i;
                return res;
            }
            h = (h + 1) & (HASH_SIZE - 1);
        }
        /* 没找到，把 nums[i] 存进去 */
        h = (unsigned int)((long long)nums[i] * 2654435761LL) & (HASH_SIZE - 1);
        while (used[h] && keys[h] != nums[i]) h = (h + 1) & (HASH_SIZE - 1);
        used[h] = true;
        keys[h] = nums[i];
        vals[h] = i;
    }
    *returnSize = 0;
    return res;
}
