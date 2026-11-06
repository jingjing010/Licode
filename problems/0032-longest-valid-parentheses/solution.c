/* 栈保存下标，栈底为最后一个未匹配的 ')' 的下标，O(n) */
int longestValidParentheses(char* s) {
    int n = (int)strlen(s);
    int* st = (int*)malloc(sizeof(int) * (n + 1));
    int top = 0, best = 0;
    st[top++] = -1;
    for (int i = 0; i < n; i++) {
        if (s[i] == '(') {
            st[top++] = i;
        } else {
            top--;
            if (top == 0) st[top++] = i;
            else if (i - st[top - 1] > best) best = i - st[top - 1];
        }
    }
    free(st);
    return best;
}
