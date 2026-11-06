int main(void) {
    int n;
    char** words = oj_read_string_array(&n);
    oj_print_int(maxProduct(words, n));
    return 0;
}
