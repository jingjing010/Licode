int binaryGap(int n) {
    int last = -1, best = 0, pos = 0;
    while (n) {
        if (n & 1) {
            if (last >= 0 && pos - last > best)
                best = pos - last;
            last = pos;
        }
        n >>= 1;
        ++pos;
    }
    return best;
}
