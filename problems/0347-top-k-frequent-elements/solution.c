/* 计数 + 桶排序，O(n + 值域) */
#define OFFSET 10000
#define RANGE (2 * OFFSET + 1)

int* topKFrequent(int* nums, int numsSize, int k, int* returnSize) {
    static int cnt[RANGE];
    memset(cnt, 0, sizeof(cnt));
    for (int i = 0; i < numsSize; i++) cnt[nums[i] + OFFSET]++;

    /* head[c]：出现 c 次的第一个数值；nxt[v]：同一桶里的下一个数值（链表） */
    int* head = (int*)malloc(sizeof(int) * (numsSize + 1));
    static int nxt[RANGE];
    for (int c = 0; c <= numsSize; c++) head[c] = -1;
    for (int v = 0; v < RANGE; v++) {
        if (cnt[v] > 0) {
            nxt[v] = head[cnt[v]];
            head[cnt[v]] = v;
        }
    }
    int* res = (int*)malloc(sizeof(int) * k);
    int m = 0;
    for (int c = numsSize; c >= 1 && m < k; c--) {
        for (int v = head[c]; v != -1 && m < k; v = nxt[v]) res[m++] = v - OFFSET;
    }
    free(head);
    *returnSize = m;
    return res;
}
