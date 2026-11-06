/* 四平方和定理 + 勒让德三平方和定理，O(sqrt(n)) */
static int isSquare(int x) {
    int r = (int)sqrt((double)x);
    while (r * r > x) r--;
    while ((r + 1) * (r + 1) <= x) r++;
    return r * r == x;
}

int numSquares(int n) {
    if (isSquare(n)) return 1;
    int m = n;
    while (m % 4 == 0) m /= 4;
    if (m % 8 == 7) return 4;
    for (int i = 1; i * i < n; i++)
        if (isSquare(n - i * i)) return 2;
    return 3;
}
