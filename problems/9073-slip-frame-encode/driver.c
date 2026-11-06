int main(void) {
    int dataSize;
    int *raw_data = oj_read_int_array(&dataSize);
    uint8_t *data = malloc(dataSize ? dataSize : 1);
    for (int i = 0; i < dataSize; ++i) {
        if (raw_data[i] < 0 || raw_data[i] > 255)
            oj_fail("字节越界");
        data[i] = (uint8_t)raw_data[i];
    }
    int returnSize = 0;
    int *out = slipEncode(data, dataSize, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    free(raw_data);
    free(data);
    return 0;
}
