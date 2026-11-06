int main(void) {
    uint32_t bitmap = (uint32_t)oj_read_ll();
    int width = (int)oj_read_ll();
    oj_print_int(longestFreeRun(bitmap, width));
    return 0;
}
