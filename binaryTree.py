## 输入某二叉树的前序遍历和中序遍历的结果，构建该二叉树并返回其根节点。

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode: # 值为 TreeNode
        def recur(root, left, right): # 根节点在前序遍历中的位置 root，左右子树在中序遍历中的左边界 left 与右边界 right
            if left > right:
                return # 递归终止
            node = TreeNode(preorder[root]) # 通过前序遍历定位根节点
            i = dic[preorder[root]] # 通过根节点在 (中序遍历定义的) dic 中的索引找到左子树的右边界
            node.left = recur(root + 1, left, i - 1) # 开启左子树递归
            node.right = recur(i - left + root + 1, i + 1, right) # 开启右子树递归
            return node # 回溯返回根节点

        dic, preorder = {}, preorder # 定义 dic
        for i in range(len(inorder)):
            dic[inorder[i]] = i # 通过中序遍历赋索引值
        return recur(0, 0, len(inorder) - 1) # 返回结果


## 输入两棵二叉树A和B，判断B是不是A的子结构。(约定空树不是任意一个树的子结构)

class Solution:
    def isSubStructure(self, A: TreeNode, B: TreeNode) -> bool: # 值为 bool
        def recur(A, B):  # 树的结构是否匹配
            if not B:
                return True # 如果节点 B 为空，说明 B 匹配完成，返回 True
            if not A or A.val != B.val:
                return False # 如果节点 A 为空，说明越过数 A 的叶子节点，匹配失败；如果 A 的值不等于 B 的值，也返回 False
            return recur(A.left, B.left) and recur(A.right, B.right) # 返回 A，B 的左右子树是否匹配

        return bool(A and B) and (recur(A, B) or self.isSubStructure(A.left, B) or self.isSubStructure(A.right, B))
        # 返回 (A,B 非空) 并且 (A,B 匹配) 或者 (A 的左子树与 B 匹配) 或者右子树与 B 匹配


## 请完成一个函数，输入一个二叉树，该函数输出它的镜像。

class Solution:
    def mirrorTree(self, root: TreeNode) -> TreeNode:
        if not root:
            return  # 如果为空，返回
        root.left, root.right = self.mirrorTree(root.right), self.mirrorTree(root.left)
        # 对根节点的右子数和左子树做镜像，然后做左右子节点的交换
        return root


## 请实现一个函数，用来判断一棵二叉树是不是对称的。如果一棵二叉树和它的镜像一样，那么它是对称的。

class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        def recur(L, R):  # 左半边节点 L 和右半边节点 R
            if not L and not R:
                return True # 如果 L 和 R 同时为空，返回 True
            if not L or not R or L.val != R.val:
                return False  # 如果 L 或 R 为空 (两者都空上面已经返回 True)，或者 L.val != R.val，返回 False
            return recur(L.left, R.right) and recur(L.right, R.left)
            # 返回 L.left-R.right and L.right-R.left 是否匹配 (对称)

        return recur(root.left, root.right) if root else True # 初始的 L=root.left，R=root.right，如果 root 非空那么返回 recur 否则直接返回 True


## 从上到下按层打印二叉树，同一层的节点按从左到右的顺序打印，每一层打印到一行。
## 利用队列实现
class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root:
            return [] # 空
        res, queue = [], collections.deque() # 定义队列
        queue.append(root) # 根节点入队
        while queue:
            tmp = [] # 存储每行节点值
            for _ in range(len(queue)):
                node = queue.popleft() # 出队
                tmp.append(node.val) # tmp 存储出队节点值
                if node.left:
                    queue.append(node.left) # node左右节点入队
                if node.right:
                    queue.append(node.right)
            res.append(tmp) # tmp 加入队列
        return res


## 请实现一个函数按照之字形顺序打印二叉树，即第一行按照从左到右的顺序打印，第二层按照从右到左的顺序打印，第三行再按照从左到右的顺序打印，其他行以此类推。
## 同上，不同在于分奇偶层，入队方式不同
class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        if not root: return []
        res, deque = [], collections.deque([root])
        while deque:
            tmp = collections.deque()
            for _ in range(len(deque)):
                node = deque.popleft()
                if len(res) % 2:
                    tmp.appendleft(node.val) # 偶数层 -> 队列头部
                else:
                    tmp.append(node.val) # 奇数层 -> 队列尾部
                if node.left:
                    deque.append(node.left)
                if node.right:
                    deque.append(node.right)
            res.append(list(tmp))
        return res


## 输入一个整数数组，判断该数组是不是某二叉搜索树的后序遍历结果。如果是则返回 true，否则返回 false。假设输入的数组的任意两个数字都互不相同。
# 二叉搜索树：左<根<右
class Solution:
    def verifyPostorder(self, postorder: [int]) -> bool:

        def recur(i, j):
            if i >= j:
                return True # 终止条件
            p = i
            while postorder[p] < postorder[j]:
                p += 1
            m = p # 定位右子树位置 m，根据前一个 while，左子树<根节点成立
            while postorder[p] > postorder[j]:
                p += 1 # 看右边第一个小于等于根的位置，如果最终的 p=j，返回 True
            return p == j and recur(i, m - 1) and recur(m, j - 1)

        return recur(0, len(postorder) - 1)


## 给你二叉树的根节点 root 和一个整数目标和 targetSum ，找出所有 从根节点到叶子节点 路径总和等于给定目标和的路径。
class Solution:
    def pathSum(self, root: TreeNode, sum: int) -> List[List[int]]:
        res, path = [], []
        def recur(root, tar):
            if not root: return # 终止条件
            path.append(root.val) # path 加入 root.val
            tar -= root.val # tar-当前值，如果为0，并且到叶子，表明 path 上的值加起来=target
            if tar == 0 and not root.left and not root.right:
                res.append(list(path)) # res 加上当前满足条件的 path
            recur(root.left, tar) # 递归
            recur(root.right, tar)
            path.pop() # 清空当前 path
        recur(root, sum)
        return res


## 输入一棵二叉搜索树，将该二叉搜索树转换成一个排序的循环双向链表。要求不能创建任何新的节点，只能调整树中节点指针的指向。
## 二叉搜索树，左 < 根 < 右，因此需要先递归左，修改当前指针，递归右
class Solution:
    def treeToDoublyList(self, root: 'Node') -> 'Node':
        def dfs(cur):
            if not cur:
                return # 终止条件

            dfs(cur.left)  # 递归左子树

            if self.pre:  # 修改节点引用
                self.pre.right, cur.left = cur, self.pre
            else:
                self.head = cur # 前驱节点为空，记录头节点

            self.pre = cur  # 保存 cur
            dfs(cur.right)  # 递归右子树

        if not root: return
        self.pre = None
        dfs(root)
        self.head.left, self.pre.right = self.pre, self.head # 此时 head 记录头节点、pre 记录尾节点，连接头尾
        return self.head


## 请实现两个函数，分别用来序列化和反序列化二叉树。只需要保证一个二叉树可以被序列化为一个字符串并且将这个字符串反序列化为原始的树结构。
## 采用层序遍历，此时序列化是可逆的。层序遍历需要通过队列实现。
class Codec:

    def serialize(self, root): # 将二叉树序列化为字符串
        if not root:
            return "[]"

        queue = collections.deque() # 定义队列
        queue.append(root)
        res = [] # 结果列表
        while queue:
            node = queue.popleft() # 将队列左端抛出
            if node:
                res.append(str(node.val)) # 存当前值
                queue.append(node.left) # 左子节点入队
                queue.append(node.right) # 右子节点入队
            else:
                res.append("null") # 存当前值 'null'
        return '[' + ','.join(res) + ']' # 返回字符串

    def deserialize(self, data): # 重构二叉树
        if data == "[]":
            return

        vals, i = data[1:-1].split(','), 1 # vals 为输入字符串 data 去掉首尾的'[' ']'
        root = TreeNode(int(vals[0])) # 根节点存入 vals[0]
        queue = collections.deque() # 定义队列
        queue.append(root) # 根节点入队
        while queue:
            node = queue.popleft() # 当前节点出队
            ## 这里 vals 为层序遍历，vals[i] 后面跟的是左右子节点
            if vals[i] != "null": # 如果当前值不为空
                node.left = TreeNode(int(vals[i])) # 当前节点的左子节点为 vals[i]
                queue.append(node.left) # 左子节点入队
            i += 1
            if vals[i] != "null":
                node.right = TreeNode(int(vals[i]))
                queue.append(node.right)
            i += 1
        return root