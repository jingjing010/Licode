/* 计数数组（值域 0~1000），O(n + m) */
int* intersect(int* nums1, int nums1Size, int* nums2, int nums2Size, int* returnSize) {
    int cnt[1001] = {0};
    for (int i = 0; i < nums1Size; i++) cnt[nums1[i]]++;
    int* res = (int*)malloc(sizeof(int) * (nums1Size < nums2Size ? nums1Size : nums2Size));
    int k = 0;
    for (int j = 0; j < nums2Size; j++) {
        if (cnt[nums2[j]] > 0) {
            cnt[nums2[j]]--;
            res[k++] = nums2[j];
        }
    }
    *returnSize = k;
    return res;
}
