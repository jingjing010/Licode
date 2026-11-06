int *relativeSortArray(int *arr1, int arr1Size, int *arr2, int arr2Size, int *returnSize) {
    int counts[1001] = {0}, k = 0, *out = malloc(arr1Size * sizeof(int));
    for (int i = 0; i < arr1Size; ++i)
        ++counts[arr1[i]];
    for (int i = 0; i < arr2Size; ++i)
        while (counts[arr2[i]] > 0) {
            out[k++] = arr2[i];
            --counts[arr2[i]];
        }
    /* 未指定相对次序的元素按数值升序放到末尾。 */
    for (int x = 0; x <= 1000; ++x)
        while (counts[x] > 0) {
            out[k++] = x;
            --counts[x];
        }
    *returnSize = k;
    return out;
}
