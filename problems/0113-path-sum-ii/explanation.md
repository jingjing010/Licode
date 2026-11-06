# 113. 路径总和 II —— 小白详细题解

> 第 112 题只问"有没有"，这道题要把"所有的"都找出来。新知识点是**回溯**：用一个数组记录当前路径，进去时放入、出来时拿掉。

---

## 📖 第一步：先读懂题目

用大白话说就是：

> 把所有"从根走到叶子、路上的数加起来等于 `targetSum`"的路径都列出来，每条路径写成一个数组。

示例 1：`targetSum = 22`

```
          5
         / \
        4   8
       /   / \
      11  13  4
     /  \    / \
    7    2  5   1
```

| 根到叶子的路径 | 和 | 要吗 |
|---|---|---|
| 5 → 4 → 11 → 7 | 27 | ❌ |
| 5 → 4 → 11 → 2 | 22 | ✅ |
| 5 → 8 → 13 | 26 | ❌ |
| 5 → 8 → 4 → 5 | 22 | ✅ |
| 5 → 8 → 4 → 1 | 18 | ❌ |

答案 `[[5,4,11,2],[5,8,4,5]]`。

**几个需要注意的细节：**

1. 和第 112 题一样，路径必须**到叶子**才算。示例 3 `[1,2]`、target = 0：没有任何路径和为 0，返回空。
2. 答案顺序任意（本 OJ 会排序后比较），但**每条路径内部**必须是从根到叶子的顺序。
3. 有负数，不能"超过就停"。
4. 返回值是二维数组，三样东西都要准备：数组本身、每行长度 `*returnColumnSizes`、行数 `*returnSize`。

---

## 🧰 第二步：这道题需要的 C 语言知识

### 1. 全局（`static`）变量在多个函数间共享

递归函数需要共享"当前路径""答案数组""答案个数"。参数一个个传太啰嗦，可以写成文件内的全局变量：

```c
static int path[5000];   // 当前路径
static int pathLen;      // 当前路径长度
```

⚠️ 判题时你的函数可能被调用多次（力扣就是这样），所以**每次进入 `pathSum` 都要把它们重新初始化**。

### 2. `memcpy` 复制数组

找到一条答案时，`path` 里的内容马上会被后面的递归改掉，所以必须**复制一份**：

```c
int* row = (int*)malloc(sizeof(int) * pathLen);
memcpy(row, path, sizeof(int) * pathLen);   // 把 pathLen 个 int 复制过去
```

`memcpy(目标, 来源, 字节数)`，第三个参数是**字节数**，别忘了乘 `sizeof(int)`。

### 3. 回溯

"进入一个结点时 `path[pathLen++] = val`，离开时 `pathLen--`"。这样 `path` 就始终等于"从根到当前结点"的路径，不需要每层都拷贝一份。

---

## 💡 第三步：思路一 —— DFS + 回溯

### 思路

1. 进入结点：把值放进 `path` 末尾，`rest` 减去这个值。
2. 如果是叶子并且 `rest == 0`：复制 `path` 存进答案。
3. 否则递归左子树、右子树。
4. 离开结点：`pathLen--`（把自己从路径里拿掉），把 `path` 恢复成进来之前的样子。

### 手动模拟（示例 1 的前半部分）

| 动作 | path | rest |
|---|---|---|
| 进入 5 | [5] | 17 |
| 进入 4 | [5,4] | 13 |
| 进入 11 | [5,4,11] | 2 |
| 进入 7（叶子，rest = -5 ≠ 0） | [5,4,11,7] | -5 |
| 离开 7 | [5,4,11] | |
| 进入 2（叶子，rest = 0 ✅ 记录） | [5,4,11,2] | 0 |
| 离开 2、离开 11、离开 4 | [5] | |
| 进入 8 …… | [5,8] | 9 |

`rest` 是值传递的参数，回到上一层自动恢复，不需要手动加回去；只有共享的 `path` 需要手动 `pathLen--`。

### 代码

```c
#define MAXN 5000

static int path[MAXN];     // 当前从根到某结点的路径
static int pathLen;        // path 中有几个数
static int** res;          // 答案
static int* cols;          // 每条答案路径的长度
static int cnt;            // 答案条数

static void dfs(struct TreeNode* node, int rest) {
    if (node == NULL) return;
    path[pathLen++] = node->val;               // 1. 进入：放进路径
    rest -= node->val;
    if (node->left == NULL && node->right == NULL) {
        if (rest == 0) {                       // 2. 叶子且正好凑齐：复制一份存起来
            int* row = (int*)malloc(sizeof(int) * pathLen);
            memcpy(row, path, sizeof(int) * pathLen);
            res[cnt] = row;
            cols[cnt] = pathLen;
            cnt++;
        }
    } else {
        dfs(node->left, rest);                 // 3. 去左右子树继续找
        dfs(node->right, rest);
    }
    pathLen--;                                 // 4. 离开：从路径中拿掉自己（回溯）
}

int** pathSum(struct TreeNode* root, int targetSum, int* returnSize, int** returnColumnSizes) {
    // 答案条数不超过叶子数，叶子数不超过结点数 5000
    res = (int**)malloc(sizeof(int*) * MAXN);
    cols = (int*)malloc(sizeof(int) * MAXN);
    cnt = 0;                                   // 每次调用都要重新初始化
    pathLen = 0;
    dfs(root, targetSum);
    *returnSize = cnt;
    *returnColumnSizes = cols;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n + 输出总长度)**：遍历每个结点一次，再加上复制答案的开销。最坏情况下（例如很多叶子都挂在一条长链下面），输出总长度可达 O(n²)，这是答案本身的大小，无法避免。
- **空间复杂度 O(h)**：递归栈和 `path`（不算答案本身）。

---

## 🚀 第四步：思路二 —— BFS + 记录父亲（不用回溯）

### 思路

按层遍历时没法"回退"，那就换个办法：给每个入队的结点记下**它的父亲在队列中的下标**和**根到它的路径和**。遇到满足条件的叶子时，顺着父亲下标一路往上走回根，就能拼出整条路径（拼出来是倒的，反着写进数组即可）。

队列里每个位置 `i` 存三样东西：`q[i]`（结点）、`sum[i]`（根到它的和）、`par[i]`（父亲的下标，根为 -1）。

### 手动模拟（示例 2：`[1,2,3]`, target = 5）

| 下标 | 结点 | sum | par |
|---|---|---|---|
| 0 | 1 | 1 | -1 |
| 1 | 2 | 3 | 0 |
| 2 | 3 | 4 | 0 |

叶子 2、3 的 sum 都不是 5，答案为空。如果 target 是 4，就从下标 2 往回走：3 → 1，反过来得到 `[1,3]`。

### 代码

```c
int** pathSum(struct TreeNode* root, int targetSum, int* returnSize, int** returnColumnSizes) {
    int** res = (int**)malloc(sizeof(int*) * 5000);
    int* cols = (int*)malloc(sizeof(int) * 5000);
    int cnt = 0;
    *returnSize = 0;
    *returnColumnSizes = cols;
    if (root == NULL) return res;

    struct TreeNode** q = (struct TreeNode**)malloc(sizeof(struct TreeNode*) * 5000);
    int* sum = (int*)malloc(sizeof(int) * 5000);     // 根到 q[i] 的路径和
    int* par = (int*)malloc(sizeof(int) * 5000);     // q[i] 的父亲在队列中的下标
    int* dep = (int*)malloc(sizeof(int) * 5000);     // q[i] 的深度（路径长度）
    int head = 0, tail = 0;
    q[tail] = root; sum[tail] = root->val; par[tail] = -1; dep[tail] = 1; tail++;

    while (head < tail) {
        int i = head++;
        struct TreeNode* node = q[i];
        if (node->left == NULL && node->right == NULL) {
            if (sum[i] == targetSum) {
                int len = dep[i];
                int* row = (int*)malloc(sizeof(int) * len);
                // 从叶子往根走，倒着填
                for (int k = i, pos = len - 1; k != -1; k = par[k], pos--) row[pos] = q[k]->val;
                res[cnt] = row;
                cols[cnt] = len;
                cnt++;
            }
            continue;
        }
        struct TreeNode* kids[2] = {node->left, node->right};
        for (int j = 0; j < 2; j++) {
            if (kids[j] == NULL) continue;
            q[tail] = kids[j];
            sum[tail] = sum[i] + kids[j]->val;
            par[tail] = i;
            dep[tail] = dep[i] + 1;
            tail++;
        }
    }
    free(q); free(sum); free(par); free(dep);
    *returnSize = cnt;
    return res;
}
```

### 复杂度分析

- **时间复杂度 O(n + 输出总长度)**：和思路一相同。
- **空间复杂度 O(n)**：队列和三个辅助数组。

---

## ⚠️ 第五步：小白常见错误

1. **直接把 `path` 指针存进答案**：
   ```c
   res[cnt] = path;   // ❌ 所有答案都指向同一块内存，最后内容全被改乱
   ```
   必须 `malloc` 新数组并 `memcpy`。
2. **忘了回溯 `pathLen--`**：路径越来越长，后面的答案里会混进别的分支的结点。注意叶子结点也要执行 `pathLen--`，所以别在找到答案后直接 `return`。
3. **全局变量没有在 `pathSum` 里重新初始化**：只在定义时写 `static int cnt = 0;`，函数第二次被调用时 `cnt` 还是上次的值。
4. **`memcpy` 第三个参数只写了 `pathLen`**：那只复制了 `pathLen` 个**字节**，也就是 `pathLen / 4` 个 `int`。
5. **在空结点处判断答案**：`if (node == NULL && rest == 0)` 会把只有一个孩子的结点当成路径终点，而且同一条路径会被左右两个空孩子各记录一次。

---

## 📊 第六步：两种方法对比

| 方法 | 时间复杂度 | 额外空间 | 难度 | 建议 |
|---|---|---|---|---|
| DFS + 回溯 | O(n + 输出) | O(h) | ⭐⭐ | **首选**，回溯模板必须掌握 |
| BFS + 父指针 | O(n + 输出) | O(n) | ⭐⭐⭐ | 了解"记录父亲还原路径"的技巧 |

---

## 🔗 举一反三

- **112. 路径总和**：只判断是否存在。
- **257. 二叉树的所有路径**：把所有根到叶子的路径都输出成字符串，同样是回溯。
- **437. 路径总和 III**：路径可以从任意结点开始。
- **46. 全排列 / 78. 子集**：经典回溯题，套路完全一样："放入 → 递归 → 拿掉"。
- **思考题**：如果要输出的不是所有路径，而是"满足条件的路径有几条"，还需要 `path` 数组吗？
