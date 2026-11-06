bool rotateString(char *s, char *goal) {
    int n = (int)strlen(s);
    if (n != (int)strlen(goal))
        return false;
    char *twice = malloc(2 * n + 1);
    memcpy(twice, s, n);
    memcpy(twice + n, s, n + 1);
    /* 任意旋转都在s+s中作为长度n的子串出现。 */
    bool found = strstr(twice, goal) != NULL;
    free(twice);
    return found;
}
