int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    int k = oj_read_int();
    oj_print_int(findKthLargest(nums, n, k));
    return 0;
}
