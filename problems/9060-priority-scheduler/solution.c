static const uint32_t* g_arrive;

static int cmpArrive(const void* a, const void* b) {
    int x = *(const int*)a, y = *(const int*)b;
    if (g_arrive[x] != g_arrive[y]) return g_arrive[x] < g_arrive[y] ? -1 : 1;
    return x - y;
}

int* prioritySchedule(const uint8_t* priority, const uint32_t* arrive, const uint16_t* burst,
                      size_t n, int* returnSize) {
    /* 时间线总长度不超过 max(arrive) + sum(burst) */
    uint32_t maxArrive = 0, total = 0;
    for (size_t i = 0; i < n; i++) {
        if (arrive[i] > maxArrive) maxArrive = arrive[i];
        total += burst[i];
    }
    uint32_t maxT = maxArrive + total;
    int* res = (int*)malloc(sizeof(int) * (maxT + 1));

    /* 按 (到达时间, 编号) 排序 */
    int* order = (int*)malloc(sizeof(int) * n);
    for (size_t i = 0; i < n; i++) order[i] = (int)i;
    g_arrive = arrive;
    qsort(order, n, sizeof(int), cmpArrive);

    /* 每个优先级一个 FIFO 就绪队列 */
    int* queue[32];
    int head[32], tail[32], cnt[32];
    memset(cnt, 0, sizeof(cnt));
    for (size_t i = 0; i < n; i++) cnt[priority[i]]++;
    for (int p = 0; p < 32; p++) {
        queue[p] = (int*)malloc(sizeof(int) * (cnt[p] + 1));
        head[p] = tail[p] = 0;
    }
    int* remain = (int*)malloc(sizeof(int) * n);
    for (size_t i = 0; i < n; i++) remain[i] = burst[i];

    uint32_t readyMask = 0;
    size_t next = 0, done = 0;
    int t = 0;
    while (done < n) {
        while (next < n && arrive[order[next]] <= (uint32_t)t) {
            int id = order[next++];
            int p = priority[id];
            queue[p][tail[p]++] = id;
            readyMask |= 1u << p;
        }
        if (readyMask == 0) {
            res[t++] = -1;
            continue;
        }
        int p = 31 - __builtin_clz(readyMask);
        int id = queue[p][head[p]];
        res[t++] = id;
        if (--remain[id] == 0) {
            head[p]++;
            done++;
            if (head[p] == tail[p]) readyMask &= ~(1u << p);
        }
    }

    for (int p = 0; p < 32; p++) free(queue[p]);
    free(order);
    free(remain);
    *returnSize = t;
    return res;
}
