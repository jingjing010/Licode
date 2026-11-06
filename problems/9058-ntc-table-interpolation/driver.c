int main(void) {
    int n, m, q;
    int* a = oj_read_int_array(&n);
    int* t = oj_read_int_array(&m);
    int* qs = oj_read_int_array(&q);
    if (n != m || n == 0) oj_fail("两张表长度必须相同且不为空");
    uint16_t* adcTable = (uint16_t*)malloc(sizeof(uint16_t) * n);
    int16_t* tempTable = (int16_t*)malloc(sizeof(int16_t) * n);
    for (int i = 0; i < n; i++) {
        adcTable[i] = (uint16_t)a[i];
        tempTable[i] = (int16_t)t[i];
    }
    int* res = (int*)malloc(sizeof(int) * (q + 1));
    for (int j = 0; j < q; j++) res[j] = ntcLookup(adcTable, tempTable, (size_t)n, (uint16_t)qs[j]);
    oj_print_int_array(res, q);
    return 0;
}
