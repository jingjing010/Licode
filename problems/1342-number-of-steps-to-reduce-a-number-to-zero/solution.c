/* 二进制：1 的个数 + 位数 - 1，O(log num) */
int numberOfSteps(int num) {
    if (num == 0) return 0;
    int ones = 0, bits = 0;
    while (num > 0) {
        ones += num & 1;
        bits++;
        num >>= 1;
    }
    return ones + bits - 1;
}
