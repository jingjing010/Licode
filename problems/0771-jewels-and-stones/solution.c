int numJewelsInStones(char *jewels, char *stones) {
    bool isJewel[256] = {false};
    for (int i = 0; jewels[i]; ++i)
        isJewel[(unsigned char)jewels[i]] = true;
    int answer = 0;
    for (int i = 0; stones[i]; ++i)
        answer += isJewel[(unsigned char)stones[i]];
    return answer;
}
