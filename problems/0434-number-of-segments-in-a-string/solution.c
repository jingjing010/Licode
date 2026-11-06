int countSegments(char *s) {
    int count = 0;
    /* 非空格字符且前一位置为空格或边界，就是新片段起点。 */
    for (int i = 0; s[i]; ++i)
        if (s[i] != ' ' && (i == 0 || s[i - 1] == ' '))
            ++count;
    return count;
}
