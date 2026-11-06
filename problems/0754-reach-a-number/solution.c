int reachNumber(int target) {
    long long t = target;
    if (t < 0)
        t = -t;
    long long sum = 0;
    int k = 0;
    /* 反转一步方向会使总位移减少该步长的两倍。 */
    while (sum < t || (sum - t) % 2 != 0)
        sum += ++k;
    return k;
}
