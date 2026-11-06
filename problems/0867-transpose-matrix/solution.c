/* 新建 n x m 矩阵，ans[j][i] = matrix[i][j]，O(mn) */
int** transpose(int** matrix, int matrixSize, int* matrixColSize, int* returnSize, int** returnColumnSizes) {
    int m = matrixSize, n = matrixColSize[0];
    int** ans = (int**)malloc(sizeof(int*) * n);
    *returnColumnSizes = (int*)malloc(sizeof(int) * n);
    for (int j = 0; j < n; j++) {
        ans[j] = (int*)malloc(sizeof(int) * m);
        (*returnColumnSizes)[j] = m;
    }
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            ans[j][i] = matrix[i][j];
    *returnSize = n;
    return ans;
}
