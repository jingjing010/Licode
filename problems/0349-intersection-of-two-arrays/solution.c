/* 标记数组（值域 0~1000），O(n + m) */
int* intersection(int* nums1, int nums1Size, int* nums2, int nums2Size, int* returnSize) {
    bool in1[1001] = {false};
    for (int i = 0; i < nums1Size; i++) in1[nums1[i]] = true;
    int* res = (int*)malloc(sizeof(int) * (nums1Size < nums2Size ? nums1Size : nums2Size));
    int k = 0;
    for (int j = 0; j < nums2Size; j++) {
        if (in1[nums2[j]]) {
            res[k++] = nums2[j];
            in1[nums2[j]] = false;
        }
    }
    *returnSize = k;
    return res;
}
