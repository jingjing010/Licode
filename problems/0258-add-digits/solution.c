int addDigits(int num) {
    /* 十进制数与各位和模9同余，0单独处理。 */
    return num == 0 ? 0 : 1 + (num - 1) % 9;
}
