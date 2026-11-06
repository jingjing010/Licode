int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    int k = removeDuplicates(nums, n);
    oj_print_int(k);
    int shown = k;              /* 防止返回值越界导致崩溃 */
    if (shown < 0) shown = 0;
    if (shown > n) shown = n;
    oj_print_int_array(nums, shown);
    return 0;
}
