int main(void) {
    uint32_t value = (uint32_t)oj_read_ll();
    int returnSize = 0;
    int *out = uleb128Encode(value, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    return 0;
}
