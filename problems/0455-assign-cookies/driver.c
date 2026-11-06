int main(void) {
    int gSize;
    int *g = oj_read_int_array(&gSize);
    int sSize;
    int *s = oj_read_int_array(&sSize);
    oj_print_int(findContentChildren(g, gSize, s, sSize));
    free(g);
    free(s);
    return 0;
}
