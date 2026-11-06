int totalMoney(int n) {
    int weeks = n / 7, days = n % 7;
    /* 完整周每周比前一周多存7元，余下天数再求等差和。 */
    return weeks * 28 + 7 * weeks * (weeks - 1) / 2 + days * (weeks + 1) + days * (days - 1) / 2;
}
