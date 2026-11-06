int main(void) {
    int n1, n2, n3;
    int* p = oj_read_int_array(&n1);
    int* a = oj_read_int_array(&n2);
    int* b = oj_read_int_array(&n3);
    if (n1 != n2 || n2 != n3) oj_fail("三个数组长度必须相同");
    uint8_t* prio = (uint8_t*)malloc(n1 + 1);
    uint32_t* arr = (uint32_t*)malloc(sizeof(uint32_t) * (n1 + 1));
    uint16_t* bur = (uint16_t*)malloc(sizeof(uint16_t) * (n1 + 1));
    for (int i = 0; i < n1; i++) {
        prio[i] = (uint8_t)p[i];
        arr[i] = (uint32_t)a[i];
        bur[i] = (uint16_t)b[i];
    }
    int sz = 0;
    int* res = prioritySchedule(prio, arr, bur, (size_t)n1, &sz);
    if (res == NULL) sz = 0;
    oj_print_int_array(res, sz);
    return 0;
}
