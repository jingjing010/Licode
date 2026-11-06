bool isPalindrome(int x) {
    /* 负数没有回文表示，只反转低半部分避免溢出。 */
    if (x < 0 || (x != 0 && x % 10 == 0))
        return false;
    int reversed = 0;
    while (x > reversed) {
        reversed = reversed * 10 + x % 10;
        x /= 10;
    }
    return x == reversed || x == reversed / 10;
}
