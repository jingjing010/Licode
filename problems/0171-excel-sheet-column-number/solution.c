int titleToNumber(char *columnTitle) {
    int answer = 0;
    /* 每追加一位，已有结果乘26，再加当前1到26的数字。 */
    for (int i = 0; columnTitle[i]; ++i)
        answer = answer * 26 + columnTitle[i] - 'A' + 1;
    return answer;
}
