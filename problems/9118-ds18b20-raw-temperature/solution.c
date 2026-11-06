int ds18b20MilliC(int raw) {
    /* 用显式减65536解释补码，避免实现相关的窄类型转换。 */
    int signedRaw = raw >= 32768 ? raw - 65536 : raw;
    return signedRaw * 1000 / 16;
}
