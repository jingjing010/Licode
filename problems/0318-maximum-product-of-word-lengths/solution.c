int maxProduct(char** words, int wordsSize) {
    int* mask = (int*)malloc(sizeof(int) * wordsSize);
    int* len = (int*)malloc(sizeof(int) * wordsSize);
    for (int i = 0; i < wordsSize; i++) {
        int m = 0, k = 0;
        for (; words[i][k]; k++) m |= 1 << (words[i][k] - 'a');
        mask[i] = m;
        len[i] = k;
    }
    int best = 0;
    for (int i = 0; i < wordsSize; i++) {
        for (int j = i + 1; j < wordsSize; j++) {
            if ((mask[i] & mask[j]) == 0 && len[i] * len[j] > best) best = len[i] * len[j];
        }
    }
    free(mask);
    free(len);
    return best;
}
