int evalRPN(char** tokens, int tokensSize) {
    int* st = (int*)malloc(sizeof(int) * tokensSize);
    int top = 0;
    for (int i = 0; i < tokensSize; i++) {
        char* t = tokens[i];
        if (t[1] == '\0' && (t[0] == '+' || t[0] == '-' || t[0] == '*' || t[0] == '/')) {
            int b = st[--top];
            int a = st[--top];
            int r;
            if (t[0] == '+') r = a + b;
            else if (t[0] == '-') r = a - b;
            else if (t[0] == '*') r = a * b;
            else r = a / b;
            st[top++] = r;
        } else {
            st[top++] = atoi(t);
        }
    }
    int ans = st[0];
    free(st);
    return ans;
}
