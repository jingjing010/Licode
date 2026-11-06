uint16_t internetChecksum(const uint8_t *data, size_t len) {
    uint32_t sum = 0;
    size_t i = 0;
    for (; i + 1 < len; i += 2)
        sum += ((uint32_t)data[i] << 8) | data[i + 1];
    if (i < len)
        sum += (uint32_t)data[i] << 8;
    /* 高16位的进位回卷到低16位，然后按位取反。 */
    while (sum >> 16)
        sum = (sum & 0xffffu) + (sum >> 16);
    return (uint16_t)~sum;
}
