int main(void) {
    char *word1 = oj_read_string();
    char *word2 = oj_read_string();
    char *out = mergeAlternately(word1, word2);
    oj_print_string(out ? out : "");
    free(out);
    free(word1);
    free(word2);
    return 0;
}
