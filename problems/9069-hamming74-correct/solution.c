int hamming74Decode(int word) {
    int syndrome = 0;
    for (int p = 1; p <= 4; p *= 2) {
        int parity = 0;
        for (int i = 1; i <= 7; ++i)
            if (i & p)
                parity ^= (word >> (i - 1)) & 1;
        if (parity)
            syndrome |= p;
    }
    if (syndrome)
        word ^= 1 << (syndrome - 1);
    return ((word >> 2) & 1) | (((word >> 4) & 1) << 1) | (((word >> 5) & 1) << 2) |
           (((word >> 6) & 1) << 3);
}
