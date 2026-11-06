int findLucky(int *arr, int arrSize) {
    int counts[501] = {0};
    for (int i = 0; i < arrSize; ++i)
        ++counts[arr[i]];
    for (int x = 500; x >= 1; --x)
        if (counts[x] == x)
            return x;
    return -1;
}
