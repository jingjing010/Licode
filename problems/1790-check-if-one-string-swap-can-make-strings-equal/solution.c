bool areAlmostEqual(char *s1, char *s2) {
    int first = -1, second = -1, count = 0;
    for (int i = 0; s1[i]; ++i)
        if (s1[i] != s2[i]) {
            if (count == 0)
                first = i;
            else if (count == 1)
                second = i;
            if (++count > 2)
                return false;
        }
    return count == 0 || (count == 2 && s1[first] == s2[second] && s1[second] == s2[first]);
}
