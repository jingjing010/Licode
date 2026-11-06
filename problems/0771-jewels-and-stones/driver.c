int main(void) {
    char *jewels = oj_read_string();
    char *stones = oj_read_string();
    oj_print_int(numJewelsInStones(jewels, stones));
    free(jewels);
    free(stones);
    return 0;
}
