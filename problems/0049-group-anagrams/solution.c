/* 计数排序生成 key + 哈希表（开放寻址）分组，O(n * k) */
#define HASH_SIZE 32768 /* 2 的幂，且大于 2 * 10^4 */

static unsigned int hashStr(const char* s) {
    unsigned int h = 5381;
    while (*s) h = h * 33 + (unsigned char)*s++;
    return h;
}

char*** groupAnagrams(char** strs, int strsSize, int* returnSize, int** returnColumnSizes) {
    static int table[HASH_SIZE];
    for (int i = 0; i < HASH_SIZE; i++) table[i] = -1;

    char** keys = (char**)malloc(sizeof(char*) * strsSize);
    int* groupOf = (int*)malloc(sizeof(int) * strsSize);
    int* cnt = (int*)calloc(strsSize, sizeof(int));
    int groups = 0;

    for (int i = 0; i < strsSize; i++) {
        int len = strlen(strs[i]);
        int c[26] = {0};
        for (int j = 0; j < len; j++) c[strs[i][j] - 'a']++;
        char* key = (char*)malloc(len + 1);
        int p = 0;
        for (int ch = 0; ch < 26; ch++)
            for (int t = 0; t < c[ch]; t++) key[p++] = (char)('a' + ch);
        key[p] = '\0';

        unsigned int h = hashStr(key) & (HASH_SIZE - 1);
        while (table[h] != -1 && strcmp(keys[table[h]], key) != 0) h = (h + 1) & (HASH_SIZE - 1);
        if (table[h] == -1) {
            table[h] = groups;
            keys[groups++] = key;
        } else {
            free(key);
        }
        groupOf[i] = table[h];
        cnt[groupOf[i]]++;
    }

    char*** res = (char***)malloc(sizeof(char**) * groups);
    int* cols = (int*)malloc(sizeof(int) * groups);
    for (int g = 0; g < groups; g++) {
        res[g] = (char**)malloc(sizeof(char*) * cnt[g]);
        cols[g] = 0;
    }
    for (int i = 0; i < strsSize; i++) {
        int g = groupOf[i];
        res[g][cols[g]++] = strs[i];
    }

    for (int g = 0; g < groups; g++) free(keys[g]);
    free(keys);
    free(groupOf);
    free(cnt);
    *returnSize = groups;
    *returnColumnSizes = cols;
    return res;
}
