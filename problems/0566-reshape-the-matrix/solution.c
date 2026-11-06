int** matrixReshape(int** mat, int matSize, int* matColSize, int r, int c, int* returnSize, int** returnColumnSizes) {
    int m = matSize, n = matColSize[0];
    if (m * n != r * c) {
        *returnSize = m;
        *returnColumnSizes = matColSize;
        return mat;
    }
    int** res = (int**)malloc(sizeof(int*) * r);
    *returnColumnSizes = (int*)malloc(sizeof(int) * r);
    for (int i = 0; i < r; i++) {
        res[i] = (int*)malloc(sizeof(int) * c);
        (*returnColumnSizes)[i] = c;
    }
    for (int k = 0; k < m * n; k++) res[k / c][k % c] = mat[k / n][k % n];
    *returnSize = r;
    return res;
}
