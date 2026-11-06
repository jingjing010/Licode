int main(void) {
    int priority = (int)oj_read_ll();
    int node = (int)oj_read_ll();
    int message = (int)oj_read_ll();
    oj_print_int(composeCanId(priority, node, message));
    return 0;
}
