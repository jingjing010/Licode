int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    sortColors(nums, n);
    oj_print_int_array(nums, n);
    return 0;
}
