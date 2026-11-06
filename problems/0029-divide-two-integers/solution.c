int divide(int dividend, int divisor) {
    if (dividend == INT_MIN && divisor == -1) return INT_MAX;
    bool neg = (dividend < 0) != (divisor < 0);
    unsigned int a = dividend < 0 ? 0u - (unsigned int)dividend : (unsigned int)dividend;
    unsigned int b = divisor < 0 ? 0u - (unsigned int)divisor : (unsigned int)divisor;
    unsigned int q = 0;
    for (int i = 31; i >= 0; i--) {
        if ((a >> i) >= b) {
            a -= b << i;
            q |= 1u << i;
        }
    }
    return neg ? (int)(0u - q) : (int)q;
}
