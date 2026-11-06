int main(void) {
    int samplesSize;
    int *samples = oj_read_int_array(&samplesSize);
    int returnSize = 0;
    int *out = firThreeTap(samples, samplesSize, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    free(samples);
    return 0;
}
