int zeroCrossings(int *samples, int samplesSize) {
    int last = 0, count = 0;
    for (int i = 0; i < samplesSize; ++i) {
        if (samples[i] == 0)
            continue;
        int sign = samples[i] > 0 ? 1 : -1;
        if (last && sign != last)
            ++count;
        last = sign;
    }
    return count;
}
