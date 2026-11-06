int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    moveZeroes(nums, n);
    oj_print_int_array(nums, n);
    return 0;
}
