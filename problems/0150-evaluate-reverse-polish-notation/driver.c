int main(void) {
    int n;
    char** tokens = oj_read_string_array(&n);
    oj_print_int(evalRPN(tokens, n));
    return 0;
}
