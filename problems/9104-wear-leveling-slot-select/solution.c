int chooseWearSlot(int *counts, int countsSize) {
    int best = 0;
    for (int i = 1; i < countsSize; ++i)
        if (counts[i] < counts[best])
            best = i;
    return best;
}
