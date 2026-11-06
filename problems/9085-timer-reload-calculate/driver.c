int main(void) {
    int clockHz = (int)oj_read_ll();
    int prescaler = (int)oj_read_ll();
    int frequency = (int)oj_read_ll();
    oj_print_int(timerReload(clockHz, prescaler, frequency));
    return 0;
}
