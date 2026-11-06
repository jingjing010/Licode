int main(void) {
    int n;
    int* arr = oj_read_int_array(&n);
    oj_print_int(sumSubarrayMins(arr, n));
    return 0;
}
