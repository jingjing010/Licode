bool isValid(char* s) {
    int n = strlen(s);
    char* st = (char*)malloc(n + 1);
    int top = 0;
    for (int i = 0; i < n; i++) {
        st[top++] = s[i];
        if (top >= 3 && st[top - 3] == 'a' && st[top - 2] == 'b' && st[top - 1] == 'c') top -= 3;
    }
    free(st);
    return top == 0;
}
