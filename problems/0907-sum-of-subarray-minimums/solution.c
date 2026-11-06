int sumSubarrayMins(int* arr, int arrSize) {
    const long long MOD = 1000000007LL;
    int n = arrSize;
    int* left = (int*)malloc(sizeof(int) * n);
    int* right = (int*)malloc(sizeof(int) * n);
    int* st = (int*)malloc(sizeof(int) * n);
    int top = 0;
    for (int i = 0; i < n; i++) {
        while (top > 0 && arr[st[top - 1]] >= arr[i]) top--;
        left[i] = top > 0 ? st[top - 1] : -1;
        st[top++] = i;
    }
    top = 0;
    for (int i = n - 1; i >= 0; i--) {
        while (top > 0 && arr[st[top - 1]] > arr[i]) top--;
        right[i] = top > 0 ? st[top - 1] : n;
        st[top++] = i;
    }
    long long ans = 0;
    for (int i = 0; i < n; i++) {
        ans = (ans + (long long)arr[i] * (i - left[i]) % MOD * (right[i] - i)) % MOD;
    }
    free(left);
    free(right);
    free(st);
    return (int)ans;
}
