static int cmp(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}
int findContentChildren(int *g, int gSize, int *s, int sSize) {
    qsort(g, gSize, sizeof(int), cmp);
    qsort(s, sSize, sizeof(int), cmp);
    int child = 0;
    /* 每次用最小可用饼干满足最小胃口。 */
    for (int i = 0; i < sSize && child < gSize; ++i)
        if (s[i] >= g[child])
            ++child;
    return child;
}
