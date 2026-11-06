int calibrateSensor(int raw, int raw0, int raw1, int value0, int value1) {
    int64_t numerator = (int64_t)(raw - raw0) * (value1 - value0);
    return value0 + (int)(numerator / (raw1 - raw0));
}
