bool checkPerfectNumber(int num) {
    if (num <= 1)
        return false;
    long long sum = 1;
    /* 约数成对累加，平方根只能计算一次。 */
    for (int d = 2; d <= num / d; ++d)
        if (num % d == 0) {
            sum += d;
            if (d != num / d)
                sum += num / d;
        }
    return sum == num;
}
