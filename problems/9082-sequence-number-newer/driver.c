int main(void) {
    int candidate = (int)oj_read_ll();
    int reference = (int)oj_read_ll();
    oj_print_bool(sequenceNewer(candidate, reference));
    return 0;
}
