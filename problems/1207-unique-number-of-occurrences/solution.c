bool uniqueOccurrences(int *arr, int arrSize) {
    int counts[2001] = {0};
    bool seen[1001] = {false};
    for (int i = 0; i < arrSize; ++i)
        ++counts[arr[i] + 1000];
    /* 先数值计数，再检查各非零次数是否重复。 */
    for (int i = 0; i < 2001; ++i)
        if (counts[i]) {
            if (seen[counts[i]])
                return false;
            seen[counts[i]] = true;
        }
    return true;
}
