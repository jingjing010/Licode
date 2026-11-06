int main(void) {
    int n;
    int* weights = oj_read_int_array(&n);
    int days = oj_read_int();
    oj_print_int(shipWithinDays(weights, n, days));
    return 0;
}
