typedef struct Trie {
    struct Trie* child[26];
    bool isEnd;
} Trie;

Trie* trieCreate() {
    return (Trie*)calloc(1, sizeof(Trie));
}

void trieInsert(Trie* obj, char* word) {
    for (; *word; word++) {
        int c = *word - 'a';
        if (!obj->child[c]) obj->child[c] = trieCreate();
        obj = obj->child[c];
    }
    obj->isEnd = true;
}

static Trie* trieWalk(Trie* obj, const char* s) {
    for (; *s && obj; s++) obj = obj->child[*s - 'a'];
    return obj;
}

bool trieSearch(Trie* obj, char* word) {
    Trie* t = trieWalk(obj, word);
    return t && t->isEnd;
}

bool trieStartsWith(Trie* obj, char* prefix) {
    return trieWalk(obj, prefix) != NULL;
}

void trieFree(Trie* obj) {
    if (!obj) return;
    for (int i = 0; i < 26; i++) trieFree(obj->child[i]);
    free(obj);
}
