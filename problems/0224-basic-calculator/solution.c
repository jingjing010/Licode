int calculate(char* s) {
    int n = (int)strlen(s);
    int* ops = (int*)malloc(sizeof(int) * (n + 2));
    int top = 0;
    ops[top++] = 1;
    int sign = 1;
    long long ret = 0;
    int i = 0;
    while (i < n) {
        char c = s[i];
        if (c == ' ') {
            i++;
        } else if (c == '+') {
            sign = ops[top - 1];
            i++;
        } else if (c == '-') {
            sign = -ops[top - 1];
            i++;
        } else if (c == '(') {
            ops[top++] = sign;
            i++;
        } else if (c == ')') {
            top--;
            i++;
        } else {
            long long num = 0;
            while (i < n && s[i] >= '0' && s[i] <= '9') {
                num = num * 10 + (s[i] - '0');
                i++;
            }
            ret += sign * num;
        }
    }
    free(ops);
    return (int)ret;
}
