int* countBits(int n, int* returnSize) {
    int* ans = (int*)malloc(sizeof(int) * (n + 1));
    ans[0] = 0;
    for (int i = 1; i <= n; i++) ans[i] = ans[i >> 1] + (i & 1);
    *returnSize = n + 1;
    return ans;
}
