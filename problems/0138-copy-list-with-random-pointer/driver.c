/* 解析 [[7,null],[13,0]]：vals[i] 为值，rnd[i] 为 random 下标（null 记为 -1） */
static int drv_parse(const char* p, int** vals, int** rnd) {
    int cap = 16, n = 0;
    int* v = (int*)malloc(sizeof(int) * cap);
    int* r = (int*)malloc(sizeof(int) * cap);
    while (*p && *p != '[') p++;
    if (*p != '[') oj_fail("期望形如 [[7,null],[13,0]] 的输入");
    p++;
    while (*p) {
        while (*p == ' ' || *p == ',') p++;
        if (*p == ']' || !*p) break;
        if (*p != '[') oj_fail("每个结点应写成 [val,random_index]");
        p++;
        char* end;
        long x = strtol(p, &end, 10);
        if (end == p) oj_fail("结点值不合法");
        p = end;
        while (*p == ' ' || *p == ',') p++;
        long y = -1;
        if (strncmp(p, "null", 4) == 0) {
            p += 4;
        } else {
            y = strtol(p, &end, 10);
            if (end == p) oj_fail("random_index 不合法");
            p = end;
        }
        while (*p == ' ') p++;
        if (*p != ']') oj_fail("每个结点应写成 [val,random_index]");
        p++;
        if (n == cap) {
            cap *= 2;
            v = (int*)realloc(v, sizeof(int) * cap);
            r = (int*)realloc(r, sizeof(int) * cap);
        }
        v[n] = (int)x;
        r[n] = (int)y;
        n++;
    }
    for (int i = 0; i < n; i++)
        if (r[i] < -1 || r[i] >= n) oj_fail("random_index 越界");
    *vals = v;
    *rnd = r;
    return n;
}

int main(void) {
    int *vals, *rnd;
    int n = drv_parse(oj_must_line(), &vals, &rnd);
    struct Node* orig = (struct Node*)malloc(sizeof(struct Node) * (n > 0 ? n : 1));
    for (int i = 0; i < n; i++) {
        orig[i].val = vals[i];
        orig[i].next = (i + 1 < n) ? &orig[i + 1] : NULL;
        orig[i].random = rnd[i] >= 0 ? &orig[rnd[i]] : NULL;
    }
    struct Node* head = n > 0 ? &orig[0] : NULL;

    struct Node* copy = copyRandomList(head);

    for (int i = 0; i < n; i++) {
        if (orig[i].val != vals[i] || orig[i].next != ((i + 1 < n) ? &orig[i + 1] : NULL) ||
            orig[i].random != (rnd[i] >= 0 ? &orig[rnd[i]] : NULL)) {
            printf("错误：原链表被修改了（返回前必须恢复原链表）\n");
            return 0;
        }
    }
    struct Node** cp = (struct Node**)malloc(sizeof(struct Node*) * (n + 1));
    int m = 0;
    for (struct Node* p = copy; p; p = p->next) {
        if (p >= orig && p < orig + n) {
            printf("错误：复制链表中包含原链表的结点（需要 malloc 新结点）\n");
            return 0;
        }
        if (m == n) {
            printf("错误：复制链表的长度比原链表长（或者有环）\n");
            return 0;
        }
        cp[m++] = p;
    }
    if (m != n) {
        printf("错误：复制链表的长度是 %d，原链表是 %d\n", m, n);
        return 0;
    }
    putchar('[');
    for (int i = 0; i < n; i++) {
        struct Node* r = cp[i]->random;
        int idx = -1;
        if (r) {
            for (int j = 0; j < n; j++)
                if (cp[j] == r) { idx = j; break; }
            if (idx < 0) {
                printf("\n错误：第 %d 个结点的 random 没有指向复制链表中的结点\n", i);
                return 0;
            }
        }
        if (i) putchar(',');
        if (idx >= 0) printf("[%d,%d]", cp[i]->val, idx);
        else printf("[%d,null]", cp[i]->val);
    }
    printf("]\n");
    return 0;
}
