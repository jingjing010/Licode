bool judgeSquareSum(int c) {
    long long a = 0, b = (long long)sqrt((double)c);
    while (a <= b) {
        long long v = a * a + b * b;
        if (v == c)
            return true;
        /* 和太小时增加小数，和太大时减少大数。 */
        if (v < c)
            ++a;
        else
            --b;
    }
    return false;
}
