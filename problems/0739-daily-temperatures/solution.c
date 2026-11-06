int* dailyTemperatures(int* temperatures, int temperaturesSize, int* returnSize) {
    int n = temperaturesSize;
    int* ans = (int*)calloc(n, sizeof(int));
    int* stack = (int*)malloc(sizeof(int) * n);
    int top = 0;
    for (int i = 0; i < n; i++) {
        while (top > 0 && temperatures[stack[top - 1]] < temperatures[i]) {
            int j = stack[--top];
            ans[j] = i - j;
        }
        stack[top++] = i;
    }
    free(stack);
    *returnSize = n;
    return ans;
}
