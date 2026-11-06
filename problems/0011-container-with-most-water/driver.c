int main(void) {
    int n;
    int* height = oj_read_int_array(&n);
    oj_print_int(maxArea(height, n));
    return 0;
}
