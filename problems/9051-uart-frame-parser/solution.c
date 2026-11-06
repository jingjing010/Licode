typedef enum { WAIT_AA, WAIT_55, READ_LEN, READ_DATA, READ_CHK } ParseState;

int** parseFrames(const uint8_t* buf, size_t len, int* returnSize, int** returnColumnSizes) {
    size_t maxFrames = len / 4 + 1;
    int** res = (int**)malloc(sizeof(int*) * maxFrames);
    int* cols = (int*)malloc(sizeof(int) * maxFrames);
    int n = 0;

    ParseState st = WAIT_AA;
    uint8_t frameLen = 0, sum = 0;
    int got = 0;
    int* data = NULL;

    for (size_t i = 0; i < len; i++) {
        uint8_t c = buf[i];
        switch (st) {
        case WAIT_AA:
            if (c == 0xAA) st = WAIT_55;
            break;
        case WAIT_55:
            if (c == 0x55) st = READ_LEN;
            else if (c != 0xAA) st = WAIT_AA;
            break;
        case READ_LEN:
            frameLen = c;
            sum = c;
            got = 0;
            data = (int*)malloc(sizeof(int) * (frameLen + 1));
            st = (frameLen == 0) ? READ_CHK : READ_DATA;
            break;
        case READ_DATA:
            data[got++] = c;
            sum = (uint8_t)(sum + c);
            if (got == frameLen) st = READ_CHK;
            break;
        case READ_CHK:
            if (c == sum) {
                res[n] = data;
                cols[n] = frameLen;
                n++;
            } else {
                free(data);
            }
            data = NULL;
            st = WAIT_AA;
            break;
        }
    }
    free(data);
    *returnSize = n;
    *returnColumnSizes = cols;
    return res;
}
