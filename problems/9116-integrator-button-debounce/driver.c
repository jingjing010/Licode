int main(void) {
    int samplesSize;
    int *samples = oj_read_int_array(&samplesSize);
    int limit = (int)oj_read_ll();
    int returnSize = 0;
    int *out = integratorDebounce(samples, samplesSize, limit, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    free(samples);
    return 0;
}
