int maxDepth(char *s) {
    int depth = 0, best = 0;
    for (int i = 0; s[i]; ++i) {
        if (s[i] == '(') {
            ++depth;
            if (depth > best)
                best = depth;
        } else if (s[i] == ')')
            --depth;
    }
    return best;
}
