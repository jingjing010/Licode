int sumOddLengthSubarrays(int *arr, int arrSize) {
    int answer = 0;
    for (int i = 0; i < arrSize; ++i) {
        /* 包含位置i的区间共有(i+1)*(n-i)个，其中向上取半为奇长。 */
        int count = ((i + 1) * (arrSize - i) + 1) / 2;
        answer += count * arr[i];
    }
    return answer;
}
