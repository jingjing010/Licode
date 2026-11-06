typedef struct {
    int* data;
    int* mins;
    int top;
    int cap;
} MinStack;


MinStack* minStackCreate() {
    MinStack* obj = (MinStack*)malloc(sizeof(MinStack));
    obj->cap = 16;
    obj->top = 0;
    obj->data = (int*)malloc(sizeof(int) * obj->cap);
    obj->mins = (int*)malloc(sizeof(int) * obj->cap);
    return obj;
}

void minStackPush(MinStack* obj, int val) {
    if (obj->top == obj->cap) {
        obj->cap *= 2;
        obj->data = (int*)realloc(obj->data, sizeof(int) * obj->cap);
        obj->mins = (int*)realloc(obj->mins, sizeof(int) * obj->cap);
    }
    int m = val;
    if (obj->top > 0 && obj->mins[obj->top - 1] < m) m = obj->mins[obj->top - 1];
    obj->data[obj->top] = val;
    obj->mins[obj->top] = m;
    obj->top++;
}

void minStackPop(MinStack* obj) {
    obj->top--;
}

int minStackTop(MinStack* obj) {
    return obj->data[obj->top - 1];
}

int minStackGetMin(MinStack* obj) {
    return obj->mins[obj->top - 1];
}

void minStackFree(MinStack* obj) {
    free(obj->data);
    free(obj->mins);
    free(obj);
}
