int* plusOne(int* digits, int digitsSize, int* returnSize) {
    for (int i = digitsSize - 1; i >= 0; i--) {
        if (digits[i] < 9) {
            int* res = (int*)malloc(sizeof(int) * digitsSize);
            memcpy(res, digits, sizeof(int) * digitsSize);
            res[i]++;
            for (int j = i + 1; j < digitsSize; j++) res[j] = 0;
            *returnSize = digitsSize;
            return res;
        }
    }
    int* res = (int*)calloc(digitsSize + 1, sizeof(int));
    res[0] = 1;
    *returnSize = digitsSize + 1;
    return res;
}
