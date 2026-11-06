int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    int target = oj_read_int();
    int returnSize = 0;
    int* ans = searchRange(nums, n, target, &returnSize);
    if (ans == NULL) returnSize = 0;
    oj_print_int_array(ans, returnSize);
    return 0;
}
