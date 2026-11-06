int uartDivisor(int clockHz, int baud) {
    int64_t denominator = (int64_t)baud * 16;
    return (int)(((int64_t)clockHz + denominator / 2) / denominator);
}
