int *addBcdMinutes(int hourBcd, int minuteBcd, int delta, int *returnSize) {
    int h = (hourBcd >> 4) * 10 + (hourBcd & 15), m = (minuteBcd >> 4) * 10 + (minuteBcd & 15);
    int total = (h * 60 + m + delta) % 1440;
    h = total / 60;
    m = total % 60;
    int *out = malloc(2 * sizeof(int));
    out[0] = (h / 10) * 16 + h % 10;
    out[1] = (m / 10) * 16 + m % 10;
    *returnSize = 2;
    return out;
}
