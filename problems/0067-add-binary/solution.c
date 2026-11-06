char* addBinary(char* a, char* b) {
    int i = strlen(a) - 1, j = strlen(b) - 1;
    int cap = (i > j ? i : j) + 2;
    char* res = (char*)malloc(cap + 1);
    int k = cap;
    res[k] = '\0';
    int carry = 0;
    while (i >= 0 || j >= 0 || carry) {
        int sum = carry;
        if (i >= 0) sum += a[i--] - '0';
        if (j >= 0) sum += b[j--] - '0';
        res[--k] = (char)('0' + sum % 2);
        carry = sum / 2;
    }
    if (k > 0) memmove(res, res + k, cap - k + 1);
    return res;
}
