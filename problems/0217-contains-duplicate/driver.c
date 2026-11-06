int main(void) {
    int numsSize;
    int *nums = oj_read_int_array(&numsSize);
    oj_print_bool(containsDuplicate(nums, numsSize));
    free(nums);
    return 0;
}
