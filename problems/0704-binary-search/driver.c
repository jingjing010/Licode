int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    int target = oj_read_int();
    oj_print_int(search(nums, n, target));
    return 0;
}
