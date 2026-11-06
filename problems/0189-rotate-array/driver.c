int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    int k = oj_read_int();
    rotate(nums, n, k);
    oj_print_int_array(nums, n);
    return 0;
}
