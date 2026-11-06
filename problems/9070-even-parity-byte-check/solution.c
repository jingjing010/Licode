bool checkEvenParity(int data, int parity) {
    unsigned x = (unsigned)data;
    int p = parity;
    while (x) {
        p ^= (int)(x & 1u);
        x >>= 1;
    }
    return p == 0;
}
