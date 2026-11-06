int countDigits(int num) {
    int count = 0;
    /* 使用原始整数判断整除，不能用已经截断的x。 */
    for (int x = num; x; x /= 10)
        if (num % (x % 10) == 0)
            ++count;
    return count;
}
