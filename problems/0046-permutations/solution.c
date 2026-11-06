static void pm_dfs(int* nums, int n, int depth, int* path, bool* used, int** res, int* cnt) {
    if (depth == n) {
        res[*cnt] = (int*)malloc(sizeof(int) * n);
        memcpy(res[*cnt], path, sizeof(int) * n);
        (*cnt)++;
        return;
    }
    for (int i = 0; i < n; i++) {
        if (used[i]) continue;
        used[i] = true;
        path[depth] = nums[i];
        pm_dfs(nums, n, depth + 1, path, used, res, cnt);
        used[i] = false;
    }
}

int** permute(int* nums, int numsSize, int* returnSize, int** returnColumnSizes) {
    int total = 1;
    for (int i = 2; i <= numsSize; i++) total *= i;
    int** res = (int**)malloc(sizeof(int*) * total);
    int path[6];
    bool used[6] = {false};
    int cnt = 0;
    pm_dfs(nums, numsSize, 0, path, used, res, &cnt);
    *returnSize = cnt;
    *returnColumnSizes = (int*)malloc(sizeof(int) * total);
    for (int i = 0; i < cnt; i++) (*returnColumnSizes)[i] = numsSize;
    return res;
}
