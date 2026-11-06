bool checkIfExist(int *arr, int arrSize) {
    bool seen[4001] = {false};
    for (int i = 0; i < arrSize; ++i) {
        int x = arr[i];
        if (seen[2 * x + 2000] || (x % 2 == 0 && seen[x / 2 + 2000]))
            return true;
        seen[x + 2000] = true;
    }
    return false;
}
