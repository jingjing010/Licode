/* 双指针，O(n) 时间 O(1) 空间 */
int trap(int* height, int heightSize) {
    int l = 0, r = heightSize - 1, lmax = 0, rmax = 0, ans = 0;
    while (l < r) {
        if (height[l] > lmax) lmax = height[l];
        if (height[r] > rmax) rmax = height[r];
        if (lmax < rmax) {
            ans += lmax - height[l];
            l++;
        } else {
            ans += rmax - height[r];
            r--;
        }
    }
    return ans;
}
