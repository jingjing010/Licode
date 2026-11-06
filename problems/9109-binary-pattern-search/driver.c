int main(void) {
    int dataSize;
    int *raw_data = oj_read_int_array(&dataSize);
    uint8_t *data = malloc(dataSize ? dataSize : 1);
    for (int i = 0; i < dataSize; ++i) {
        if (raw_data[i] < 0 || raw_data[i] > 255)
            oj_fail("字节越界");
        data[i] = (uint8_t)raw_data[i];
    }
    int patternSize;
    int *raw_pattern = oj_read_int_array(&patternSize);
    uint8_t *pattern = malloc(patternSize ? patternSize : 1);
    for (int i = 0; i < patternSize; ++i) {
        if (raw_pattern[i] < 0 || raw_pattern[i] > 255)
            oj_fail("字节越界");
        pattern[i] = (uint8_t)raw_pattern[i];
    }
    oj_print_int(findBinaryPattern(data, dataSize, pattern, patternSize));
    free(raw_data);
    free(data);
    free(raw_pattern);
    free(pattern);
    return 0;
}
