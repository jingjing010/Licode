/**
 * ADC 原始值转毫伏：mv[i] = round(raw[i] * vref_mv / (2^bits - 1))，只用整数运算。
 */
void adc_to_mv(const uint16_t* raw, uint16_t* mv, size_t len, uint8_t bits, uint16_t vref_mv) {
    
}
