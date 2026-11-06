int main(void) {
    int length = (int)oj_read_ll();
    int maximum = (int)oj_read_ll();
    int returnSize = 0;
    int *out = dmaChunks(length, maximum, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    return 0;
}
