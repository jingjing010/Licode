int i2cAddressByte(int address, int read) {
    return (address << 1) | read;
}
