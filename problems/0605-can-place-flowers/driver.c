int main(void) {
    int size;
    int *a = oj_read_int_array(&size);
    int n = oj_read_int();
    oj_print_bool(canPlaceFlowers(a, size, n));
    free(a);
    return 0;
}
