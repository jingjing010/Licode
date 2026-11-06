/* 双指针，O(n) */
int maxArea(int* height, int heightSize) {
    int l = 0, r = heightSize - 1, best = 0;
    while (l < r) {
        int h = height[l] < height[r] ? height[l] : height[r];
        int area = h * (r - l);
        if (area > best) best = area;
        if (height[l] < height[r]) l++;
        else r--;
    }
    return best;
}
