int main(void) {
    int timesSize;
    int *times = oj_read_int_array(&timesSize);
    int period = (int)oj_read_ll();
    int returnSize = 0;
    int *out = periodicReleases(times, timesSize, period, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    free(times);
    return 0;
}
