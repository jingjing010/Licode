static bool drv_is_peak(const int* a, int n, int i) {
    if (i < 0 || i >= n) return false;
    if (i > 0 && a[i] <= a[i - 1]) return false;
    if (i < n - 1 && a[i] <= a[i + 1]) return false;
    return true;
}

int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    int* copy = (int*)malloc(sizeof(int) * (n > 0 ? n : 1));
    memcpy(copy, nums, sizeof(int) * n);
    int ans = findPeakElement(nums, n);
    oj_print_bool(drv_is_peak(copy, n, ans));
    return 0;
}
