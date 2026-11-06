/* 多源 BFS：所有初始烂橘子同时入队，一层 = 一分钟，O(m*n) */
int orangesRotting(int** grid, int gridSize, int* gridColSize) {
    int m = gridSize, n = gridColSize[0];
    int* q = (int*)malloc(sizeof(int) * (m * n + 1));
    int head = 0, tail = 0, fresh = 0;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++) {
            if (grid[i][j] == 2) q[tail++] = i * n + j;
            else if (grid[i][j] == 1) fresh++;
        }
    static const int dr[4] = {1, -1, 0, 0};
    static const int dc[4] = {0, 0, 1, -1};
    int minutes = 0;
    while (head < tail && fresh > 0) {
        int levelEnd = tail;
        while (head < levelEnd) {
            int cur = q[head++];
            int r = cur / n, c = cur % n;
            for (int d = 0; d < 4; d++) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nr < m && nc >= 0 && nc < n && grid[nr][nc] == 1) {
                    grid[nr][nc] = 2;
                    fresh--;
                    q[tail++] = nr * n + nc;
                }
            }
        }
        minutes++;
    }
    free(q);
    return fresh == 0 ? minutes : -1;
}
