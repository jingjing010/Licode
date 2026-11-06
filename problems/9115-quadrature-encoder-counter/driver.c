int main(void) {
    int statesSize;
    int *states = oj_read_int_array(&statesSize);
    oj_print_int(quadratureCount(states, statesSize));
    free(states);
    return 0;
}
