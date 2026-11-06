int main(void) {
    int targetsSize;
    int *targets = oj_read_int_array(&targetsSize);
    int step = (int)oj_read_ll();
    int returnSize = 0;
    int *out = slewLimit(targets, targetsSize, step, &returnSize);
    oj_print_int_array(out, returnSize);
    free(out);
    free(targets);
    return 0;
}
