int minMoves(int *nums, int numsSize) {
    int minimum = nums[0];
    long long sum = 0;
    for (int i = 0; i < numsSize; ++i) {
        if (nums[i] < minimum)
            minimum = nums[i];
        sum += nums[i];
    }
    /* 给n-1个元素加1，相对差值等价于给另一个减1。 */
    return (int)(sum - (long long)minimum * numsSize);
}
