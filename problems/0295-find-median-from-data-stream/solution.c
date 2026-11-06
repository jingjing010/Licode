/* 两个堆：lo 是大根堆（较小的一半），hi 是小根堆（较大的一半），|lo| == |hi| 或 |lo| == |hi| + 1 */
typedef struct {
    int* lo;
    int* hi;
    int nlo;
    int nhi;
    int cap;
} MedianFinder;

/* sign = 1 表示大根堆，sign = -1 表示小根堆（比较 sign * a） */
static void mfPush(int* h, int* n, int x, int sign) {
    int i = (*n)++;
    h[i] = x;
    while (i > 0) {
        int p = (i - 1) / 2;
        if (sign * h[p] >= sign * h[i]) break;
        int t = h[p]; h[p] = h[i]; h[i] = t;
        i = p;
    }
}

static int mfPop(int* h, int* n, int sign) {
    int top = h[0];
    h[0] = h[--(*n)];
    int i = 0;
    while (1) {
        int l = 2 * i + 1, r = l + 1, best = i;
        if (l < *n && sign * h[l] > sign * h[best]) best = l;
        if (r < *n && sign * h[r] > sign * h[best]) best = r;
        if (best == i) break;
        int t = h[i]; h[i] = h[best]; h[best] = t;
        i = best;
    }
    return top;
}

MedianFinder* medianFinderCreate() {
    MedianFinder* obj = (MedianFinder*)malloc(sizeof(MedianFinder));
    obj->cap = 16;
    obj->nlo = obj->nhi = 0;
    obj->lo = (int*)malloc(sizeof(int) * obj->cap);
    obj->hi = (int*)malloc(sizeof(int) * obj->cap);
    return obj;
}

void medianFinderAddNum(MedianFinder* obj, int num) {
    if (obj->nlo + 1 > obj->cap || obj->nhi + 1 > obj->cap) {
        obj->cap *= 2;
        obj->lo = (int*)realloc(obj->lo, sizeof(int) * obj->cap);
        obj->hi = (int*)realloc(obj->hi, sizeof(int) * obj->cap);
    }
    mfPush(obj->lo, &obj->nlo, num, 1);
    mfPush(obj->hi, &obj->nhi, mfPop(obj->lo, &obj->nlo, 1), -1);
    if (obj->nhi > obj->nlo) mfPush(obj->lo, &obj->nlo, mfPop(obj->hi, &obj->nhi, -1), 1);
}

double medianFinderFindMedian(MedianFinder* obj) {
    if (obj->nlo > obj->nhi) return obj->lo[0];
    return ((double)obj->lo[0] + obj->hi[0]) / 2.0;
}

void medianFinderFree(MedianFinder* obj) {
    free(obj->lo);
    free(obj->hi);
    free(obj);
}
