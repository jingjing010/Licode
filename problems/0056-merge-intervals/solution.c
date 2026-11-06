/* 按左端点排序后一遍合并，O(n log n) */
static int cmpInterval(const void* a, const void* b) {
    const int* x = *(int* const*)a;
    const int* y = *(int* const*)b;
    if (x[0] != y[0]) return x[0] < y[0] ? -1 : 1;
    return (x[1] > y[1]) - (x[1] < y[1]);
}

int** merge(int** intervals, int intervalsSize, int* intervalsColSize, int* returnSize, int** returnColumnSizes) {
    qsort(intervals, intervalsSize, sizeof(int*), cmpInterval);
    int** res = (int**)malloc(sizeof(int*) * intervalsSize);
    int* cols = (int*)malloc(sizeof(int) * intervalsSize);
    int cnt = 0;
    for (int i = 0; i < intervalsSize; i++) {
        int l = intervals[i][0], r = intervals[i][1];
        if (cnt > 0 && l <= res[cnt - 1][1]) {
            if (r > res[cnt - 1][1]) res[cnt - 1][1] = r;
        } else {
            res[cnt] = (int*)malloc(sizeof(int) * 2);
            res[cnt][0] = l;
            res[cnt][1] = r;
            cols[cnt] = 2;
            cnt++;
        }
    }
    *returnSize = cnt;
    *returnColumnSizes = cols;
    return res;
}
