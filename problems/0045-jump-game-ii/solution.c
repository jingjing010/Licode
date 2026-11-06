/* 贪心（按层 BFS）：O(n) */
int jump(int* nums, int numsSize) {
    int steps = 0, end = 0, far = 0;
    for (int i = 0; i < numsSize - 1; i++) {
        if (i + nums[i] > far) far = i + nums[i];
        if (i == end) {
            steps++;
            end = far;
        }
    }
    return steps;
}
