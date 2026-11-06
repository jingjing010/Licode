static int cmp(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return (x > y) - (x < y);
}
int distributeCandies(int *candyType, int candyTypeSize) {
    qsort(candyType, candyTypeSize, sizeof(int), cmp);
    int kinds = 0;
    for (int i = 0; i < candyTypeSize; ++i)
        if (i == 0 || candyType[i] != candyType[i - 1])
            ++kinds;
    return kinds < candyTypeSize / 2 ? kinds : candyTypeSize / 2;
}
