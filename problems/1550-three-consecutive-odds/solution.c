bool threeConsecutiveOdds(int *arr, int arrSize) {
    int run = 0;
    for (int i = 0; i < arrSize; ++i) {
        run = arr[i] % 2 ? run + 1 : 0;
        if (run == 3)
            return true;
    }
    return false;
}
