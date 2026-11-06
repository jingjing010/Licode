/* 前缀和 + 哈希表计数，O(n) */
#define SS_HASH_SIZE (1 << 16)

static int ssKeys[SS_HASH_SIZE];
static int ssCnt[SS_HASH_SIZE];
static char ssUsed[SS_HASH_SIZE];

static unsigned int ssSlot(int x) {
    unsigned int h = ((unsigned int)x * 2654435761u) >> 16;
    while (ssUsed[h] && ssKeys[h] != x) h = (h + 1) & (SS_HASH_SIZE - 1);
    return h;
}

int subarraySum(int* nums, int numsSize, int k) {
    memset(ssUsed, 0, sizeof(ssUsed));
    unsigned int h = ssSlot(0);
    ssUsed[h] = 1;
    ssKeys[h] = 0;
    ssCnt[h] = 1;
    int pre = 0, ans = 0;
    for (int i = 0; i < numsSize; i++) {
        pre += nums[i];
        h = ssSlot(pre - k);
        if (ssUsed[h]) ans += ssCnt[h];
        h = ssSlot(pre);
        if (!ssUsed[h]) {
            ssUsed[h] = 1;
            ssKeys[h] = pre;
            ssCnt[h] = 0;
        }
        ssCnt[h]++;
    }
    return ans;
}
