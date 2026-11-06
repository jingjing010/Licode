int main(void) {
    int n;
    int* a = oj_read_int_array(&n);
    int k = oj_read_int();
    uint8_t* s = (uint8_t*)malloc(n + 1);
    for (int i = 0; i < n; i++) s[i] = (uint8_t)a[i];
    int rows = 0;
    int* cols = NULL;
    int** res = debounce(s, (size_t)n, (uint16_t)k, &rows, &cols);
    if (res == NULL || cols == NULL) rows = 0;
    oj_print_int_matrix(res, rows, cols);
    return 0;
}
