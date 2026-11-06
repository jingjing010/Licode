/* 计数排序得到标签 + 哈希表按标签分组，O(n * L) */
#define GA_HASH_SIZE (1 << 15)

static char* gaSortedKey(const char* s) {
    int cnt[26] = {0};
    int len = 0;
    for (; s[len]; len++) cnt[s[len] - 'a']++;
    char* key = (char*)malloc(len + 1);
    int p = 0;
    for (int c = 0; c < 26; c++)
        while (cnt[c]--) key[p++] = (char)('a' + c);
    key[p] = '\0';
    return key;
}

static unsigned int gaHash(const char* s) {
    unsigned int h = 2166136261u;
    for (; *s; s++) h = (h ^ (unsigned char)*s) * 16777619u;
    return h & (GA_HASH_SIZE - 1);
}

char*** groupAnagrams(char** strs, int strsSize, int* returnSize, int** returnColumnSizes) {
    static int table[GA_HASH_SIZE];
    for (int i = 0; i < GA_HASH_SIZE; i++) table[i] = -1;
    char** keys = (char**)malloc(sizeof(char*) * strsSize);
    int* gid = (int*)malloc(sizeof(int) * strsSize);
    int* first = (int*)malloc(sizeof(int) * strsSize);
    int* sizes = (int*)calloc(strsSize, sizeof(int));
    int groups = 0;
    for (int i = 0; i < strsSize; i++) {
        keys[i] = gaSortedKey(strs[i]);
        unsigned int h = gaHash(keys[i]);
        while (table[h] != -1 && strcmp(keys[first[table[h]]], keys[i]) != 0)
            h = (h + 1) & (GA_HASH_SIZE - 1);
        if (table[h] == -1) {
            table[h] = groups;
            first[groups++] = i;
        }
        gid[i] = table[h];
        sizes[gid[i]]++;
    }
    char*** res = (char***)malloc(sizeof(char**) * groups);
    int* cols = (int*)malloc(sizeof(int) * groups);
    for (int g = 0; g < groups; g++) {
        res[g] = (char**)malloc(sizeof(char*) * sizes[g]);
        cols[g] = 0;
    }
    for (int i = 0; i < strsSize; i++) {
        int g = gid[i];
        res[g][cols[g]++] = strs[i];
    }
    for (int i = 0; i < strsSize; i++) free(keys[i]);
    free(keys);
    free(gid);
    free(first);
    free(sizes);
    *returnSize = groups;
    *returnColumnSizes = cols;
    return res;
}
