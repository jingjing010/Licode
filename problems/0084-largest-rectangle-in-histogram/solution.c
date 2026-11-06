int largestRectangleArea(int* heights, int heightsSize) {
    int n = heightsSize;
    int* stack = (int*)malloc(sizeof(int) * (n + 1));
    int top = 0;
    int best = 0;
    for (int i = 0; i <= n; i++) {
        int h = (i == n) ? 0 : heights[i];
        while (top > 0 && heights[stack[top - 1]] >= h) {
            int height = heights[stack[--top]];
            int left = (top == 0) ? -1 : stack[top - 1];
            int area = height * (i - left - 1);
            if (area > best) best = area;
        }
        stack[top++] = i;
    }
    free(stack);
    return best;
}
