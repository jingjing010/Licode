bool sequenceNewer(int candidate, int reference) {
    uint16_t distance = (uint16_t)((unsigned)candidate - (unsigned)reference);
    return distance != 0 && distance < 0x8000u;
}
