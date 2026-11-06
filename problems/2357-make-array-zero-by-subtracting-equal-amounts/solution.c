int minimumOperations(int *nums, int numsSize) {
    bool seen[101] = {false};
    int answer = 0;
    /* 每次选择最小正值，恰好消去一个不同的正数层级。 */
    for (int i = 0; i < numsSize; ++i)
        if (nums[i] > 0 && !seen[nums[i]]) {
            seen[nums[i]] = true;
            ++answer;
        }
    return answer;
}
