bool isPowerOfTwo(int n) {
    /* 正的2次幂只有一个二进制位为1。 */
    return n > 0 && (n & (n - 1)) == 0;
}
