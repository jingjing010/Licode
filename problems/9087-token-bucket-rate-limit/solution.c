int *tokenBucket(int *times, int timesSize, int capacity, int interval, int *returnSize) {
    int *out = malloc((timesSize + 1) * sizeof(int)), tokens = capacity, last = 0;
    for (int i = 0; i < timesSize; ++i) {
        int add = (times[i] - last) / interval;
        last += add * interval;
        tokens = tokens + add > capacity ? capacity : tokens + add;
        out[i] = tokens > 0;
        if (tokens)
            --tokens;
    }
    *returnSize = timesSize;
    return out;
}
