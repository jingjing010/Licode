int main(void) {
    int n;
    int* nums = oj_read_int_array(&n);
    oj_print_int(findMaxConsecutiveOnes(nums, n));
    return 0;
}
