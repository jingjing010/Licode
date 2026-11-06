int main(void) {
    int n;
    int* a = oj_read_int_array(&n);
    uint8_t* buf = (uint8_t*)malloc(n + 1);
    for (int i = 0; i < n; i++) buf[i] = (uint8_t)a[i];
    int rows = 0;
    int* colSizes = NULL;
    int** frames = parseFrames(buf, (size_t)n, &rows, &colSizes);
    if (frames == NULL || colSizes == NULL) rows = 0;
    oj_print_int_matrix(frames, rows, colSizes);
    free(buf);
    return 0;
}
