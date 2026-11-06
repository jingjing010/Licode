bool hasAlternatingBits(int n) {
    uint32_t x = (uint32_t)n ^ ((uint32_t)n >> 1);
    /* 相邻位不同，异或右移一位的结果就是连续的1。 */
    return (x & (x + 1u)) == 0;
}
