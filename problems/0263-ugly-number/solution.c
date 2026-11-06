bool isUgly(int n) {
    if (n <= 0)
        return false;
    /* 删除全部2、3、5因子后不应剩下其他因子。 */
    int p[] = {2, 3, 5};
    for (int i = 0; i < 3; ++i)
        while (n % p[i] == 0)
            n /= p[i];
    return n == 1;
}
