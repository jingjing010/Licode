char* addStrings(char* num1, char* num2) {
    int i = strlen(num1) - 1, j = strlen(num2) - 1;
    int cap = (i > j ? i : j) + 2;
    char* res = (char*)malloc(cap + 1);
    int k = cap;
    res[k] = '\0';
    int carry = 0;
    while (i >= 0 || j >= 0 || carry) {
        int sum = carry;
        if (i >= 0) sum += num1[i--] - '0';
        if (j >= 0) sum += num2[j--] - '0';
        res[--k] = (char)('0' + sum % 10);
        carry = sum / 10;
    }
    if (k > 0) memmove(res, res + k, cap - k + 1);
    return res;
}
