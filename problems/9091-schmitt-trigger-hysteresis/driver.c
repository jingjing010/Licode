int main(void) {
    int samplesSize;
    int *samples = oj_read_int_array(&samplesSize);
    int low = (int)oj_read_ll();
    int high = (int)oj_read_ll();
    int returnSize = 0;
    int *out = schmittTrigger(samples, samplesSize, low, high, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    free(samples);
    return 0;
}
