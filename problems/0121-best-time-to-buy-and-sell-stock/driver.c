int main(void) {
    int n;
    int* prices = oj_read_int_array(&n);
    oj_print_int(maxProfit(prices, n));
    return 0;
}
