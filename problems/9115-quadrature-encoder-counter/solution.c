int quadratureCount(int *states, int statesSize) {
    static const int delta[16] = {0, 1, -1, 0, -1, 0, 0, 1, 1, 0, 0, -1, 0, -1, 1, 0};
    int count = 0;
    for (int i = 1; i < statesSize; ++i)
        count += delta[states[i - 1] * 4 + states[i]];
    return count;
}
