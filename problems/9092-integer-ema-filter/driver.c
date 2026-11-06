int main(void) {
    int samplesSize;
    int *samples = oj_read_int_array(&samplesSize);
    int shift = (int)oj_read_ll();
    int returnSize = 0;
    int *out = emaFilter(samples, samplesSize, shift, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    free(samples);
    return 0;
}
