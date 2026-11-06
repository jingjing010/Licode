/* 3^19 是 int 范围内最大的 3 的幂，O(1) */
bool isPowerOfThree(int n) {
    return n > 0 && 1162261467 % n == 0;
}
