int scoreOfParentheses(char* s) {
    int ans = 0, depth = 0;
    for (int i = 0; s[i]; i++) {
        if (s[i] == '(') {
            depth++;
        } else {
            depth--;
            if (s[i - 1] == '(') ans += 1 << depth;
        }
    }
    return ans;
}
