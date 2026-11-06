uint32_t composeCanId(int priority, int node, int message) {
    /* 此布局是本练习自定义的29位应用层标识符。 */
    return ((uint32_t)priority << 26) | ((uint32_t)node << 16) | (uint32_t)message;
}
