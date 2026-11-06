bool checkIfPangram(char *sentence) {
    uint32_t mask = 0;
    for (int i = 0; sentence[i]; ++i)
        mask |= 1u << (sentence[i] - 'a');
    return mask == ((1u << 26) - 1);
}
