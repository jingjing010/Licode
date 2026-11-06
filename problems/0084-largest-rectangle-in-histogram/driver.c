int main(void) {
    int n;
    int* heights = oj_read_int_array(&n);
    oj_print_int(largestRectangleArea(heights, n));
    return 0;
}
