int main(void) {
    int base = (int)oj_read_ll();
    int attempt = (int)oj_read_ll();
    int cap = (int)oj_read_ll();
    oj_print_int(retryDelay(base, attempt, cap));
    return 0;
}
