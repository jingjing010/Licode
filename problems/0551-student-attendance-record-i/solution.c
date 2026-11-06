bool checkRecord(char *s) {
    int absent = 0, late = 0;
    for (int i = 0; s[i]; ++i) {
        if (s[i] == 'A' && ++absent >= 2)
            return false;
        late = s[i] == 'L' ? late + 1 : 0;
        if (late >= 3)
            return false;
    }
    return true;
}
