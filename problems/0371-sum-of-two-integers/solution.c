int getSum(int a, int b) {
    unsigned int x = (unsigned int)a, y = (unsigned int)b;
    while (y != 0) {
        unsigned int carry = (x & y) << 1;
        x ^= y;
        y = carry;
    }
    return (int)x;
}
