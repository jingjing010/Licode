#define SOL_MAX_KEY 10001

typedef struct SolNode {
    int key, val;
    struct SolNode *prev, *next;
} SolNode;

typedef struct {
    int capacity, size;
    SolNode head, tail;
    SolNode* map[SOL_MAX_KEY];
} LRUCache;

static void sol_unlink(SolNode* x) {
    x->prev->next = x->next;
    x->next->prev = x->prev;
}

static void sol_push_front(LRUCache* obj, SolNode* x) {
    x->prev = &obj->head;
    x->next = obj->head.next;
    obj->head.next->prev = x;
    obj->head.next = x;
}

LRUCache* lRUCacheCreate(int capacity) {
    LRUCache* obj = (LRUCache*)calloc(1, sizeof(LRUCache));
    obj->capacity = capacity;
    obj->head.next = &obj->tail;
    obj->tail.prev = &obj->head;
    return obj;
}

int lRUCacheGet(LRUCache* obj, int key) {
    SolNode* x = obj->map[key];
    if (!x) return -1;
    sol_unlink(x);
    sol_push_front(obj, x);
    return x->val;
}

void lRUCachePut(LRUCache* obj, int key, int value) {
    SolNode* x = obj->map[key];
    if (x) {
        x->val = value;
        sol_unlink(x);
        sol_push_front(obj, x);
        return;
    }
    if (obj->size == obj->capacity) {
        SolNode* old = obj->tail.prev;
        sol_unlink(old);
        obj->map[old->key] = NULL;
        free(old);
        obj->size--;
    }
    x = (SolNode*)malloc(sizeof(SolNode));
    x->key = key;
    x->val = value;
    sol_push_front(obj, x);
    obj->map[key] = x;
    obj->size++;
}

void lRUCacheFree(LRUCache* obj) {
    SolNode* p = obj->head.next;
    while (p != &obj->tail) {
        SolNode* next = p->next;
        free(p);
        p = next;
    }
    free(obj);
}
