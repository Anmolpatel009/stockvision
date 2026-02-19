# Implement Trie (Prefix Tree)

**Difficulty:** Medium  
**Pattern:** Tries  
**LeetCode:** #208

## Problem Statement

A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings.

Implement the Trie class:
- `Trie()` Initializes the trie object.
- `void insert(String word)` Inserts the string word into the trie.
- `boolean search(String word)` Returns true if the string word is in the trie, and false otherwise.
- `boolean startsWith(String prefix)` Returns true if there is a previously inserted string word that has the prefix, and false otherwise.

## Examples

### Example 1:
```
Input
["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
[[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
Output
[null, null, true, false, true, null, true]

Explanation
Trie trie = new Trie();
trie.insert("apple");
trie.search("apple");   // return True
trie.search("app");     // return False
trie.startsWith("app"); // return True
trie.insert("app");
trie.search("app");     // return True
```

## Constraints

- `1 <= word.length, prefix.length <= 2000`
- `word` and `prefix` consist only of lowercase English letters.
- At most `3 * 10^4` calls in total will be made to insert, search, and startsWith.

## Solution Approaches

### Approach 1: Array-based Trie Node
**Time Complexity:** O(m) for all operations where m is key length  
**Space Complexity:** O(alphabet_size * total_nodes)

```python
class TrieNode:
    def __init__(self):
        self.children = [None] * 26
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            idx = ord(char) - ord('a')
            if not node.children[idx]:
                node.children[idx] = TrieNode()
            node = node.children[idx]
        node.is_end = True
    
    def search(self, word):
        node = self._search_prefix(word)
        return node is not None and node.is_end
    
    def startsWith(self, prefix):
        return self._search_prefix(prefix) is not None
    
    def _search_prefix(self, prefix):
        node = self.root
        for char in prefix:
            idx = ord(char) - ord('a')
            if not node.children[idx]:
                return None
            node = node.children[idx]
        return node
```

### Approach 2: Dictionary-based Trie Node
**Time Complexity:** O(m) for all operations  
**Space Complexity:** O(total_characters)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
    
    def startsWith(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
```

### Approach 3: Using Set (Simple but Less Efficient)
**Time Complexity:** O(n) for search, O(1) for insert  
**Space Complexity:** O(total_characters)

```python
class Trie:
    def __init__(self):
        self.words = set()
        self.prefixes = set()
    
    def insert(self, word):
        self.words.add(word)
        for i in range(1, len(word) + 1):
            self.prefixes.add(word[:i])
    
    def search(self, word):
        return word in self.words
    
    def startsWith(self, prefix):
        return prefix in self.prefixes
```

## Key Insights

1. **Trie stores characters** as paths from root
2. **Mark end of word** with a flag
3. **Prefix search** just checks if path exists

## Related Problems

- Add and Search Word (LeetCode #211)
- Design Add and Search Words Data Structure (LeetCode #211)
- Word Search II (LeetCode #212)