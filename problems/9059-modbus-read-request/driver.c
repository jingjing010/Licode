int main(void) {
    int slave = oj_read_int();
    int start = oj_read_int();
    int qty = oj_read_int();
    uint8_t frame[32];
    memset(frame, 0, sizeof(frame));
    size_t n = modbusBuildReadRequest((uint8_t)slave, (uint16_t)start, (uint16_t)qty, frame);
    if (n > 32) oj_fail("返回的长度不合法");
    int res[32];
    for (size_t i = 0; i < n; i++) res[i] = frame[i];
    oj_print_int_array(res, (int)n);
    return 0;
}
