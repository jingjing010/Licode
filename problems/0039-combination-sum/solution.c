static void cs_dfs(int* c, int n, int start, int remain, int* path, int len,
                   int** res, int* cols, int* cnt) {
    if (remain == 0) {
        res[*cnt] = (int*)malloc(sizeof(int) * (len + 1));
        memcpy(res[*cnt], path, sizeof(int) * len);
        cols[*cnt] = len;
        (*cnt)++;
        return;
    }
    for (int i = start; i < n && c[i] <= remain; i++) {
        path[len] = c[i];
        cs_dfs(c, n, i, remain - c[i], path, len + 1, res, cols, cnt);
    }
}

static int cs_cmp(const void* a, const void* b) {
    return *(const int*)a - *(const int*)b;
}

int** combinationSum(int* candidates, int candidatesSize, int target, int* returnSize, int** returnColumnSizes) {
    qsort(candidates, candidatesSize, sizeof(int), cs_cmp);
    int** res = (int**)malloc(sizeof(int*) * 160);
    *returnColumnSizes = (int*)malloc(sizeof(int) * 160);
    int path[24];
    *returnSize = 0;
    cs_dfs(candidates, candidatesSize, 0, target, path, 0, res, *returnColumnSizes, returnSize);
    return res;
}
