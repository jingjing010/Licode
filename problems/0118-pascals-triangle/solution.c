/* 逐行递推，O(numRows^2) */
int** generate(int numRows, int* returnSize, int** returnColumnSizes) {
    int** res = (int**)malloc(sizeof(int*) * numRows);
    *returnColumnSizes = (int*)malloc(sizeof(int) * numRows);
    for (int i = 0; i < numRows; i++) {
        res[i] = (int*)malloc(sizeof(int) * (i + 1));
        (*returnColumnSizes)[i] = i + 1;
        res[i][0] = res[i][i] = 1;
        for (int j = 1; j < i; j++) res[i][j] = res[i - 1][j - 1] + res[i - 1][j];
    }
    *returnSize = numRows;
    return res;
}
