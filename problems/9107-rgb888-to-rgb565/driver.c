int main(void) {
    int red = (int)oj_read_ll();
    int green = (int)oj_read_ll();
    int blue = (int)oj_read_ll();
    oj_print_int(rgb565(red, green, blue));
    return 0;
}
