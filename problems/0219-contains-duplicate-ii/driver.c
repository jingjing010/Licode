int main(void) {
    int numsSize;
    int *nums = oj_read_int_array(&numsSize);
    int k = (int)oj_read_ll();
    oj_print_bool(containsNearbyDuplicate(nums, numsSize, k));
    free(nums);
    return 0;
}
