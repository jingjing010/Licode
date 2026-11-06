int subtractProductAndSum(int n) {
    int product = 1, sum = 0;
    /* 乘积初值是1，加法初值是0。 */
    while (n) {
        int d = n % 10;
        product *= d;
        sum += d;
        n /= 10;
    }
    return product - sum;
}
