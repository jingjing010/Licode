/* 一次遍历：维护历史最低价，O(n) */
int maxProfit(int* prices, int pricesSize) {
    int minPrice = INT_MAX, best = 0;
    for (int i = 0; i < pricesSize; i++) {
        if (prices[i] < minPrice) minPrice = prices[i];
        else if (prices[i] - minPrice > best) best = prices[i] - minPrice;
    }
    return best;
}
