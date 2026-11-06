bool divisorGame(int n) {
    /* 偶数减1交给对手奇数；奇数只能减奇因子变成偶数。 */
    return n % 2 == 0;
}
