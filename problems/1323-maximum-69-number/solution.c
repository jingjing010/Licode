int maximum69Number(int num) {
    int x = num, place = 1, last = 0;
    /* 从低位扫描，最后记录的位置就是最高位的6。 */
    while (x) {
        if (x % 10 == 6)
            last = place;
        place *= 10;
        x /= 10;
    }
    return num + 3 * last;
}
