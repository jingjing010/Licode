int maxWidthRamp(int* nums, int numsSize) {
    int* st = (int*)malloc(sizeof(int) * numsSize);
    int top = 0;
    for (int i = 0; i < numsSize; i++) {
        if (top == 0 || nums[i] < nums[st[top - 1]]) st[top++] = i;
    }
    int ans = 0;
    for (int j = numsSize - 1; j >= 0 && top > 0; j--) {
        while (top > 0 && nums[st[top - 1]] <= nums[j]) {
            int w = j - st[--top];
            if (w > ans) ans = w;
        }
    }
    free(st);
    return ans;
}
