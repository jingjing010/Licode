int *modbusWriteSingle(int address, int reg, int value, int *returnSize) {
    int *out = malloc(8 * sizeof(int));
    out[0] = address;
    out[1] = 6;
    out[2] = reg >> 8;
    out[3] = reg & 255;
    out[4] = value >> 8;
    out[5] = value & 255;
    uint16_t crc = 0xffff;
    for (int i = 0; i < 6; ++i) {
        crc ^= (uint16_t)out[i];
        for (int b = 0; b < 8; ++b)
            crc = (crc & 1) ? (crc >> 1) ^ 0xa001 : crc >> 1;
    }
    /* 寄存器字段为大端，CRC在线上却是低字节先发。 */
    out[6] = crc & 255;
    out[7] = crc >> 8;
    *returnSize = 8;
    return out;
}
