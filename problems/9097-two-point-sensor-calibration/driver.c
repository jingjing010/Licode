int main(void) {
    int raw = (int)oj_read_ll();
    int raw0 = (int)oj_read_ll();
    int raw1 = (int)oj_read_ll();
    int value0 = (int)oj_read_ll();
    int value1 = (int)oj_read_ll();
    oj_print_int(calibrateSensor(raw, raw0, raw1, value0, value1));
    return 0;
}
