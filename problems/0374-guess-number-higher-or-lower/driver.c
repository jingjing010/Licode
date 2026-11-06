static int drv_bits(int n) {
    int b = 0;
    while (n > 0) { b++; n >>= 1; }
    return b;
}

int main(void) {
    int n = oj_read_int();
    int pick = oj_read_int();
    drv_n_range = n;
    drv_pick = pick;
    drv_calls = 0;
    drv_call_limit = 2LL * drv_bits(n) + 2;
    int ans = guessNumber(n);
    oj_print_int(ans);
    return 0;
}
