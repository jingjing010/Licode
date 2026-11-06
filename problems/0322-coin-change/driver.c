int main(void) {
    int n;
    int* coins = oj_read_int_array(&n);
    int amount = oj_read_int();
    oj_print_int(coinChange(coins, n, amount));
    return 0;
}
