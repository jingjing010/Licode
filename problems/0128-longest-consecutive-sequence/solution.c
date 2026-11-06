/* 哈希集合 + 只从序列起点往后数，O(n) */
#define LC_HASH_SIZE (1 << 18)

static int lcKeys[LC_HASH_SIZE];
static char lcUsed[LC_HASH_SIZE];

static unsigned int lcHash(int x) {
    return ((unsigned int)x * 2654435761u) >> 14;
}

static bool lcContains(int x) {
    unsigned int h = lcHash(x);
    while (lcUsed[h]) {
        if (lcKeys[h] == x) return true;
        h = (h + 1) & (LC_HASH_SIZE - 1);
    }
    return false;
}

static void lcInsert(int x) {
    unsigned int h = lcHash(x);
    while (lcUsed[h]) {
        if (lcKeys[h] == x) return;
        h = (h + 1) & (LC_HASH_SIZE - 1);
    }
    lcUsed[h] = 1;
    lcKeys[h] = x;
}

int longestConsecutive(int* nums, int numsSize) {
    memset(lcUsed, 0, sizeof(lcUsed));
    for (int i = 0; i < numsSize; i++) lcInsert(nums[i]);
    int best = 0;
    for (int h = 0; h < LC_HASH_SIZE; h++) {
        if (!lcUsed[h]) continue;
        int x = lcKeys[h];
        if (x > INT_MIN && lcContains(x - 1)) continue;
        int len = 1;
        while (x < INT_MAX && lcContains(x + 1)) {
            x++;
            len++;
        }
        if (len > best) best = len;
    }
    return best;
}
