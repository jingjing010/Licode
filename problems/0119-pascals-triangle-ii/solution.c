int* getRow(int rowIndex, int* returnSize) {
    int* row = (int*)malloc(sizeof(int) * (rowIndex + 1));
    row[0] = 1;
    for (int i = 1; i <= rowIndex; i++) {
        row[i] = (int)((long long)row[i - 1] * (rowIndex - i + 1) / i);
    }
    *returnSize = rowIndex + 1;
    return row;
}
