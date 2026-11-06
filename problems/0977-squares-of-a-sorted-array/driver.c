int main(void) {
    int numsSize;
    int *nums = oj_read_int_array(&numsSize);
    int returnSize = 0;
    int *out = sortedSquares(nums, numsSize, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    free(nums);
    return 0;
}
