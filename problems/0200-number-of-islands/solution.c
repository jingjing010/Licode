static void sink(char** grid, int m, int n, int r, int c) {
    if (r < 0 || r >= m || c < 0 || c >= n || grid[r][c] != '1') return;
    grid[r][c] = '0';
    sink(grid, m, n, r + 1, c);
    sink(grid, m, n, r - 1, c);
    sink(grid, m, n, r, c + 1);
    sink(grid, m, n, r, c - 1);
}

int numIslands(char** grid, int gridSize, int* gridColSize) {
    if (gridSize == 0) return 0;
    int m = gridSize, n = gridColSize[0], cnt = 0;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            if (grid[i][j] == '1') {
                cnt++;
                sink(grid, m, n, i, j);
            }
    return cnt;
}
