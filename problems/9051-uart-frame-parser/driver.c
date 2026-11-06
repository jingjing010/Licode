int main(void) {
    int n;
    int* a = oj_read_int_array(&n);
    uint8_t* buf = (uint8_t*)malloc(n + 1);
    for (int i = 0; i < n; i++) buf[i] = (uint8_t)a[i];
    int rows = 0;
    int* cols = NULL;
    int** res = parseFrames(buf, (size_t)n, &rows, &cols);
    if (res == NULL || cols == NULL) rows = 0;
    oj_print_int_matrix(res, rows, cols);
    return 0;
}
