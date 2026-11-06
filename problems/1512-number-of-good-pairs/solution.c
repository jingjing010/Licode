int numIdenticalPairs(int *nums, int numsSize) {
    int counts[101] = {0}, answer = 0;
    /* 当前元素与之前每个相同元素各组成一对。 */
    for (int i = 0; i < numsSize; ++i) {
        answer += counts[nums[i]];
        ++counts[nums[i]];
    }
    return answer;
}
