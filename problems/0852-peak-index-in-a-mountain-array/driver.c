int main(void) {
    int n;
    int* arr = oj_read_int_array(&n);
    oj_print_int(peakIndexInMountainArray(arr, n));
    return 0;
}
