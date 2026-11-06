int hamming74Encode(int data) {
    int d0 = data & 1, d1 = (data >> 1) & 1, d2 = (data >> 2) & 1, d3 = (data >> 3) & 1;
    /* 位置1、2、4为偶校验位，位置3、5、6、7保存数据。 */
    return (d0 ^ d1 ^ d3) | ((d0 ^ d2 ^ d3) << 1) | (d0 << 2) | ((d1 ^ d2 ^ d3) << 3) | (d1 << 4) |
           (d2 << 5) | (d3 << 6);
}
