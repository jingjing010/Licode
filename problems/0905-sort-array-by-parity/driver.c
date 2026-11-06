int main(void) {
    int n, size = 0;
    int *nums = oj_read_int_array(&n);
    int *original = malloc(n * sizeof(int));
    memcpy(original, nums, n * sizeof(int));
    int *out = sortArrayByParity(nums, n, &size);
    bool valid = size == n && out != NULL;
    int counts[5001] = {0};
    for (int i = 0; i < n; ++i) {
        if (original[i] < 0 || original[i] > 5000) oj_fail("元素超出约束");
        ++counts[original[i]];
    }
    bool odd = false;
    if (valid) for (int i = 0; i < n; ++i) {
        int x = out[i];
        if (x < 0 || x > 5000 || --counts[x] < 0) { valid = false; break; }
        if (x % 2) odd = true;
        else if (odd) { valid = false; break; }
    }
    if (!valid) oj_fail("返回数组不是偶数在前的原数组排列");
    /* 合法答案先标准化，允许任意组内顺序及原地返回。 */
    int *canonical = malloc(n * sizeof(int)), k = 0;
    for (int parity = 0; parity < 2; ++parity)
        for (int i = 0; i < n; ++i)
            if (original[i] % 2 == parity) canonical[k++] = original[i];
    oj_print_int_array(canonical, n);
    if (out != nums) free(out);
    free(nums); free(original); free(canonical);
    return 0;
}
