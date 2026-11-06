int main(void) {
    int n;
    int* timeSeries = oj_read_int_array(&n);
    int duration = oj_read_int();
    oj_print_int(findPoisonedDuration(timeSeries, n, duration));
    return 0;
}
