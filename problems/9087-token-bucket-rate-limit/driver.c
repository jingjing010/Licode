int main(void) {
    int timesSize;
    int *times = oj_read_int_array(&timesSize);
    int capacity = (int)oj_read_ll();
    int interval = (int)oj_read_ll();
    int returnSize = 0;
    int *out = tokenBucket(times, timesSize, capacity, interval, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    free(times);
    return 0;
}
