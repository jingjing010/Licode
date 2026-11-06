int main(void) {
    int n;
    char* letters = oj_read_char_array(&n);
    char* t = oj_read_string();
    char ans = nextGreatestLetter(letters, n, t[0]);
    printf("\"%c\"\n", ans);
    return 0;
}
