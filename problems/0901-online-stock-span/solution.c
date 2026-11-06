typedef struct {
    int* price;
    int* span;
    int top;
    int cap;
} StockSpanner;


StockSpanner* stockSpannerCreate() {
    StockSpanner* obj = (StockSpanner*)malloc(sizeof(StockSpanner));
    obj->cap = 16;
    obj->top = 0;
    obj->price = (int*)malloc(sizeof(int) * obj->cap);
    obj->span = (int*)malloc(sizeof(int) * obj->cap);
    return obj;
}

int stockSpannerNext(StockSpanner* obj, int price) {
    int span = 1;
    while (obj->top > 0 && obj->price[obj->top - 1] <= price) {
        obj->top--;
        span += obj->span[obj->top];
    }
    if (obj->top == obj->cap) {
        obj->cap *= 2;
        obj->price = (int*)realloc(obj->price, sizeof(int) * obj->cap);
        obj->span = (int*)realloc(obj->span, sizeof(int) * obj->cap);
    }
    obj->price[obj->top] = price;
    obj->span[obj->top] = span;
    obj->top++;
    return span;
}

void stockSpannerFree(StockSpanner* obj) {
    free(obj->price);
    free(obj->span);
    free(obj);
}
