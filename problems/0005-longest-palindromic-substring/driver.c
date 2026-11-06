static bool drv_is_palindrome(const char* p, int len) {
    for (int i = 0, j = len - 1; i < j; i++, j--)
        if (p[i] != p[j]) return false;
    return true;
}

/* 中心扩展：返回最长回文子串的长度，*start 为最靠左的那个的起点 */
static int drv_longest(const char* s, int n, int* start) {
    int best = 0;
    *start = 0;
    for (int c = 0; c < 2 * n - 1; c++) {
        int l = c / 2, r = l + c % 2;
        while (l >= 0 && r < n && s[l] == s[r]) {
            l--;
            r++;
        }
        int len = r - l - 1, st = l + 1;
        if (len > best || (len == best && st < *start)) {
            best = len;
            *start = st;
        }
    }
    return best;
}

int main(void) {
    char* s = oj_read_string();
    int n = (int)strlen(s);
    char* orig = (char*)malloc(n + 1);
    memcpy(orig, s, n + 1);

    char* ans = longestPalindrome(s);

    int start;
    int best = drv_longest(orig, n, &start);
    if (ans != NULL) {
        int len = (int)strlen(ans);
        if (len == best && drv_is_palindrome(ans, len) && strstr(orig, ans) != NULL) {
            char* canon = (char*)malloc(best + 1);
            memcpy(canon, orig + start, best);
            canon[best] = '\0';
            oj_print_string(canon);
            return 0;
        }
    }
    oj_print_string(ans ? ans : "");
    return 0;
}
