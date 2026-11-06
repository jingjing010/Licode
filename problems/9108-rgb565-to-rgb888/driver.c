int main(void) {
    int pixel = (int)oj_read_ll();
    int returnSize = 0;
    int *out = expandRgb565(pixel, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    return 0;
}
