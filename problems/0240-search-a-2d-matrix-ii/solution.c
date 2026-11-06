/* Z 字形查找：从右上角出发，O(m + n) */
bool searchMatrix(int** matrix, int matrixSize, int* matrixColSize, int target) {
    int r = 0, c = matrixColSize[0] - 1;
    while (r < matrixSize && c >= 0) {
        if (matrix[r][c] == target) return true;
        if (matrix[r][c] > target) c--;
        else r++;
    }
    return false;
}
