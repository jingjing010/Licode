int main(void) {
    int numsSize;
    int *nums = oj_read_int_array(&numsSize);
    int target = (int)oj_read_ll();
    int start = (int)oj_read_ll();
    oj_print_int(getMinDistance(nums, numsSize, target, start));
    free(nums);
    return 0;
}
