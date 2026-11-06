/* 贪心：记录每个字母最后出现的位置，O(n) */
int* partitionLabels(char* s, int* returnSize) {
    int n = (int)strlen(s);
    int last[26];
    for (int i = 0; i < n; i++) last[s[i] - 'a'] = i;
    int* res = (int*)malloc(sizeof(int) * (n > 0 ? n : 1));
    int cnt = 0, start = 0, end = 0;
    for (int i = 0; i < n; i++) {
        if (last[s[i] - 'a'] > end) end = last[s[i] - 'a'];
        if (i == end) {
            res[cnt++] = end - start + 1;
            start = i + 1;
        }
    }
    *returnSize = cnt;
    return res;
}
