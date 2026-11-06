int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    int returnSize = 0;
    int* ans = productExceptSelf(nums, n, &returnSize);
    if (ans == NULL) returnSize = 0;
    oj_print_int_array(ans, returnSize);
    return 0;
}
