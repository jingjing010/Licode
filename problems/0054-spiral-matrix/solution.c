/* 按层模拟：四条边界逐步收缩，O(mn) */
int* spiralOrder(int** matrix, int matrixSize, int* matrixColSize, int* returnSize) {
    int m = matrixSize, n = matrixColSize[0];
    int* res = (int*)malloc(sizeof(int) * m * n);
    int cnt = 0;
    int top = 0, bottom = m - 1, left = 0, right = n - 1;
    while (top <= bottom && left <= right) {
        for (int j = left; j <= right; j++) res[cnt++] = matrix[top][j];
        for (int i = top + 1; i <= bottom; i++) res[cnt++] = matrix[i][right];
        if (top < bottom && left < right) {
            for (int j = right - 1; j >= left; j--) res[cnt++] = matrix[bottom][j];
            for (int i = bottom - 1; i > top; i--) res[cnt++] = matrix[i][left];
        }
        top++;
        bottom--;
        left++;
        right--;
    }
    *returnSize = cnt;
    return res;
}
