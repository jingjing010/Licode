/* 定长滑动窗口 + 维护不同计数的字母个数，O(n) */
int* findAnagrams(char* s, char* p, int* returnSize) {
    int n = strlen(s), m = strlen(p);
    *returnSize = 0;
    int* res = (int*)malloc(sizeof(int) * (n + 1));
    if (m > n) return res;
    int diff[26] = {0};
    for (int i = 0; i < m; i++) {
        diff[s[i] - 'a']++;
        diff[p[i] - 'a']--;
    }
    int bad = 0;
    for (int c = 0; c < 26; c++) if (diff[c]) bad++;
    if (bad == 0) res[(*returnSize)++] = 0;
    for (int i = m; i < n; i++) {
        int in = s[i] - 'a', out = s[i - m] - 'a';
        if (in != out) {
            if (diff[in] == 0) bad++;
            diff[in]++;
            if (diff[in] == 0) bad--;
            if (diff[out] == 0) bad++;
            diff[out]--;
            if (diff[out] == 0) bad--;
        }
        if (bad == 0) res[(*returnSize)++] = i - m + 1;
    }
    return res;
}
