int main(void) {
    int romSize;
    int *raw_rom = oj_read_int_array(&romSize);
    uint8_t *rom = malloc(romSize ? romSize : 1);
    for (int i = 0; i < romSize; ++i) {
        if (raw_rom[i] < 0 || raw_rom[i] > 255)
            oj_fail("字节越界");
        rom[i] = (uint8_t)raw_rom[i];
    }
    oj_print_bool(validateOneWireRom(rom, romSize));
    free(raw_rom);
    free(rom);
    return 0;
}
