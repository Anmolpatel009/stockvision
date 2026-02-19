# Word Search II

**Difficulty:** Hard  
**Pattern:** Tries  
**LeetCode:** #212

## Problem Statement

Given an `m x n` board of characters and a list of strings `words`, return all words on the board.

Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.

## Examples

### Example 1:
```
Input: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
Output: ["eat","oath"]
```

### Example 2:
```
Input: board = [["a","b"],["c","d"]], words = ["abcb"]
Output: []
```

## Constraints

- `m == board.length`
- `n == board[i].length`
- `1 <= m, n <= 12`
- `board[i][j]` is a lowercase English letter.
- `1 <= words.length <= 3 * 10^4`
- `1 <= words[i].length <= 10`
- `words[i]` consists of lowercase English letters.
- All the strings of words are unique.

## Solution Approaches

### Approach 1: Trie + DFS Backtracking
**Time Complexity:** O(m * n * 4^L) where L is max word length  
**Space Complexity:** O(total_characters in words)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

class Solution:
    def findWords(self, board, words):
        # Build trie
        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.word = word
        
        result = []
        m, n = len(board), len(board[0])
        
        def dfs(i, j, node):
            char = board[i][j]
            
            if char not in node.children:
                return
            
            curr_node = node.children[char]
            
            if curr_node.word:
                result.append(curr_node.word)
                curr_node.word = None  # Avoid duplicates
            
            board[i][j] = '#'
            
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and board[ni][nj] != '#':
                    dfs(ni, nj, curr_node)
            
            board[i][j] = char
            
            # Prune: remove leaf nodes
            if not curr_node.children:
                node.children.pop(char)
        
        for i in range(m):
            for j in range(n):
                dfs(i, j, root)
        
        return result
```

### Approach 2: Simple DFS for Each Word
**Time Complexity:** O(words * m * n * 4^L)  
**Space Complexity:** O(L)

```python
def findWords(board, words):
    result = []
    m, n = len(board), len(board[0])
    
    def exist(word):
        def dfs(i, j, k):
            if k == len(word):
                return True
            if i < 0 or i >= m or j < 0 or j >= n or board[i][j] != word[k]:
                return False
            
            temp = board[i][j]
            board[i][j] = '#'
            found = (dfs(i+1, j, k+1) or dfs(i-1, j, k+1) or 
                     dfs(i, j+1, k+1) or dfs(i, j-1, k+1))
            board[i][j] = temp
            return found
        
        for i in range(m):
            for j in range(n):
                if dfs(i, j, 0):
                    return True
        return False
    
    for word in words:
        if exist(word):
            result.append(word)
    
    return result
```

### Approach 3: Trie with Early Termination
**Time Complexity:** O(m * n * 4^L)  
**Space Complexity:** O(total_characters)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.word = ""

class Solution:
    def findWords(self, board, words):
        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_end = True
            node.word = word
        
        result = []
        m, n = len(board), len(board[0])
        
        def dfs(i, j, node, path):
            if node.is_end:
                result.append(node.word)
                node.is_end = False
            
            if i < 0 or i >= m or j < 0 or j >= n:
                return
            
            char = board[i][j]
            if char not in node.children:
                return
            
            board[i][j] = '#'
            for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                dfs(i + di, j + dj, node.children[char], path + char)
            board[i][j] = char
        
        for i in range(m):
            for j in range(n):
                dfs(i, j, root, "")
        
        return result
```

## Key Insights

1. **Trie efficiently stores** all words to search
2. **DFS backtracking** explores all paths
3. **Prune trie nodes** after finding words to avoid duplicates

## Related Problems

- Word Search (LeetCode #79)
- Implement Trie (Prefix Tree) (LeetCode #208)