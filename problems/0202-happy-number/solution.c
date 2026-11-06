static int digitSquare(int x) {
    int sum = 0;
    while (x) {
        int d = x % 10;
        sum += d * d;
        x /= 10;
    }
    return sum;
}
bool isHappy(int n) {
    int slow = n, fast = n;
    /* 快慢指针检测平方和序列是否进入非1环。 */
    do {
        slow = digitSquare(slow);
        fast = digitSquare(digitSquare(fast));
    } while (slow != fast);
    return slow == 1;
}
