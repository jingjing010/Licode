int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    oj_print_bool(canPartition(nums, n));
    return 0;
}
