int q15Multiply(int a, int b) {
    int32_t scaled = (int32_t)a * b / 32768;
    if (scaled > 32767)
        return 32767;
    if (scaled < -32768)
        return -32768;
    return scaled;
}
