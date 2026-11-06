int largestAltitude(int *gain, int gainSize) {
    int height = 0, best = 0;
    for (int i = 0; i < gainSize; ++i) {
        height += gain[i];
        if (height > best)
            best = height;
    }
    return best;
}
