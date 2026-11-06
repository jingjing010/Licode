bool canFinish(int numCourses, int** prerequisites, int prerequisitesSize, int* prerequisitesColSize) {
    int n = numCourses, e = prerequisitesSize;
    int* indeg = (int*)calloc(n, sizeof(int));
    int* start = (int*)calloc(n + 1, sizeof(int));
    int* adj = (int*)malloc(sizeof(int) * (e > 0 ? e : 1));
    int* q = (int*)malloc(sizeof(int) * n);
    for (int i = 0; i < e; i++) {
        start[prerequisites[i][1] + 1]++;
        indeg[prerequisites[i][0]]++;
    }
    for (int i = 0; i < n; i++) start[i + 1] += start[i];
    int* pos = (int*)malloc(sizeof(int) * (n + 1));
    memcpy(pos, start, sizeof(int) * (n + 1));
    for (int i = 0; i < e; i++) adj[pos[prerequisites[i][1]]++] = prerequisites[i][0];
    int head = 0, tail = 0;
    for (int i = 0; i < n; i++)
        if (indeg[i] == 0) q[tail++] = i;
    while (head < tail) {
        int u = q[head++];
        for (int k = start[u]; k < start[u + 1]; k++)
            if (--indeg[adj[k]] == 0) q[tail++] = adj[k];
    }
    free(indeg); free(start); free(adj); free(q); free(pos);
    return tail == n;
}
