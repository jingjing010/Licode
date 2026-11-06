int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    int val = oj_read_int();
    int k = removeElement(nums, n, val);
    oj_print_int(k);
    int shown = k;              /* 防止返回值越界导致崩溃 */
    if (shown < 0) shown = 0;
    if (shown > n) shown = n;
    qsort(nums, shown, sizeof(int), oj_cmp_int);   /* 前 k 个元素顺序任意，排序后再比较 */
    oj_print_int_array(nums, shown);
    return 0;
}
