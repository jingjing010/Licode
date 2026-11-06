static uint16_t crc16Modbus(const uint8_t* buf, size_t len) {
    uint16_t crc = 0xFFFF;
    for (size_t i = 0; i < len; i++) {
        crc ^= buf[i];
        for (int b = 0; b < 8; b++) {
            crc = (crc & 1) ? (uint16_t)((crc >> 1) ^ 0xA001) : (uint16_t)(crc >> 1);
        }
    }
    return crc;
}

size_t modbusBuildReadRequest(uint8_t slave, uint16_t startAddr, uint16_t quantity, uint8_t* frame) {
    if (slave < 1 || slave > 247) return 0;
    if (quantity < 1 || quantity > 125) return 0;
    if ((uint32_t)startAddr + quantity > 65536u) return 0;
    frame[0] = slave;
    frame[1] = 0x03;
    frame[2] = (uint8_t)(startAddr >> 8);
    frame[3] = (uint8_t)(startAddr & 0xFF);
    frame[4] = (uint8_t)(quantity >> 8);
    frame[5] = (uint8_t)(quantity & 0xFF);
    uint16_t crc = crc16Modbus(frame, 6);
    frame[6] = (uint8_t)(crc & 0xFF);
    frame[7] = (uint8_t)(crc >> 8);
    return 8;
}
