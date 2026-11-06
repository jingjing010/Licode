int main(void) {
    int samplesSize;
    int *samples = oj_read_int_array(&samplesSize);
    oj_print_int(peakToPeak(samples, samplesSize));
    free(samples);
    return 0;
}
