bool isValid(char* s) {
    int n = (int)strlen(s);
    if (n % 2 == 1) return false;
    char* stack = (char*)malloc(n + 1);
    int top = 0;
    bool ok = true;
    for (int i = 0; i < n && ok; i++) {
        char c = s[i];
        if (c == '(' || c == '[' || c == '{') {
            stack[top++] = c;
        } else {
            char want = (c == ')') ? '(' : (c == ']') ? '[' : '{';
            if (top == 0 || stack[top - 1] != want) ok = false;
            else top--;
        }
    }
    if (top != 0) ok = false;
    free(stack);
    return ok;
}
