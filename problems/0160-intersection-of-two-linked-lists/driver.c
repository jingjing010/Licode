int main(void) {
    int intersectVal = oj_read_int();
    int m, n;
    int* a = oj_read_int_array(&m);
    int* b = oj_read_int_array(&n);
    int skipA = oj_read_int();
    int skipB = oj_read_int();
    if (skipA < 0 || skipA > m || skipB < 0 || skipB > n || m - skipA != n - skipB)
        oj_fail("skipA / skipB 不合法");
    if ((skipA < m) != (intersectVal != 0)) oj_fail("intersectVal 与 skipA 不一致");

    /* A 的全部结点 + B 独有的前 skipB 个结点；B 从第 skipB 个起与 A 的第 skipA 个起共用 */
    struct ListNode* na = (struct ListNode*)malloc(sizeof(struct ListNode) * (m > 0 ? m : 1));
    struct ListNode* nb = (struct ListNode*)malloc(sizeof(struct ListNode) * (n > 0 ? n : 1));
    for (int i = 0; i < m; i++) {
        na[i].val = a[i];
        na[i].next = (i + 1 < m) ? &na[i + 1] : NULL;
    }
    struct ListNode* common = skipA < m ? &na[skipA] : NULL;
    for (int i = 0; i < skipB; i++) {
        nb[i].val = b[i];
        nb[i].next = (i + 1 < skipB) ? &nb[i + 1] : common;
    }
    struct ListNode* headA = m > 0 ? &na[0] : NULL;
    struct ListNode* headB = skipB > 0 ? &nb[0] : common;

    struct ListNode* ans = getIntersectionNode(headA, headB);

    for (int i = 0; i < m; i++) {
        if (na[i].val != a[i] || na[i].next != ((i + 1 < m) ? &na[i + 1] : NULL)) {
            printf("错误：链表被修改了（本题要求保持链表原始结构）\n");
            return 0;
        }
    }
    for (int i = 0; i < skipB; i++) {
        if (nb[i].val != b[i] || nb[i].next != ((i + 1 < skipB) ? &nb[i + 1] : common)) {
            printf("错误：链表被修改了（本题要求保持链表原始结构）\n");
            return 0;
        }
    }
    if (ans == common) {
        if (ans) printf("Intersected at '%d'\n", ans->val);
        else printf("No intersection\n");
    } else {
        printf("错误：返回的不是相交的起始结点\n");
    }
    return 0;
}
