int findNumbers(int *nums, int numsSize) {
    int answer = 0;
    for (int i = 0; i < numsSize; ++i) {
        int digits = 0, x = nums[i];
        do {
            ++digits;
            x /= 10;
        } while (x);
        if (digits % 2 == 0)
            ++answer;
    }
    return answer;
}
