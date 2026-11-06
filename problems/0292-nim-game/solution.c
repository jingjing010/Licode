bool canWinNim(int n) {
    /* 留给对手4的倍数，就能维持每轮合计取4颗。 */
    return n % 4 != 0;
}
