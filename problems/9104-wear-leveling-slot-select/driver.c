int main(void) {
    int countsSize;
    int *counts = oj_read_int_array(&countsSize);
    oj_print_int(chooseWearSlot(counts, countsSize));
    free(counts);
    return 0;
}
