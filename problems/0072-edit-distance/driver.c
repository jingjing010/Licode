int main(void) {
    char* word1 = oj_read_string();
    char* word2 = oj_read_string();
    oj_print_int(minDistance(word1, word2));
    return 0;
}
