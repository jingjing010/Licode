int main(void) {
    int beforeSize;
    int *raw_before = oj_read_int_array(&beforeSize);
    uint8_t *before = malloc(beforeSize ? beforeSize : 1);
    for (int i = 0; i < beforeSize; ++i) {
        if (raw_before[i] < 0 || raw_before[i] > 255)
            oj_fail("字节越界");
        before[i] = (uint8_t)raw_before[i];
    }
    int afterSize;
    int *raw_after = oj_read_int_array(&afterSize);
    uint8_t *after = malloc(afterSize ? afterSize : 1);
    for (int i = 0; i < afterSize; ++i) {
        if (raw_after[i] < 0 || raw_after[i] > 255)
            oj_fail("字节越界");
        after[i] = (uint8_t)raw_after[i];
    }
    oj_print_bool(canProgramFlash(before, beforeSize, after, afterSize));
    free(raw_before);
    free(before);
    free(raw_after);
    free(after);
    return 0;
}
