/* 转置 + 每行左右翻转，O(n^2) 时间 O(1) 空间 */
void rotate(int** matrix, int matrixSize, int* matrixColSize) {
    int n = matrixSize;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) {
            int t = matrix[i][j];
            matrix[i][j] = matrix[j][i];
            matrix[j][i] = t;
        }
    for (int i = 0; i < n; i++)
        for (int l = 0, r = n - 1; l < r; l++, r--) {
            int t = matrix[i][l];
            matrix[i][l] = matrix[i][r];
            matrix[i][r] = t;
        }
}
