int main(void) {
    char *word = oj_read_string();
    int ch = (int)oj_read_ll();
    char *out = reversePrefix(word, ch);
    oj_print_string(out ? out : "");
    free(out);
    free(word);
    return 0;
}
