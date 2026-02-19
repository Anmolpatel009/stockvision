# Design Add and Search Words Data Structure

**Difficulty:** Medium  
**Pattern:** Tries  
**LeetCode:** #211

## Problem Statement

Design a data structure that supports adding new words and finding if a string matches any previously added string.

Implement the `WordDictionary` class:
- `WordDictionary()` Initializes the object.
- `void addWord(word)` Adds word to the data structure.
- `bool search(word)` Returns true if there is any string in the data structure that matches word, and false otherwise. word may contain dots '.' where a dot can be matched with any letter.

## Examples

### Example 1:
```
Input
["WordDictionary","addWord","addWord","addWord","search","search","search","search"]
[[],["bad"],["dad"],["mad"],["pad"],["bad"],[".ad"],["b.."]]
Output
[null,null,null,null,false,true,true,true]

Explanation
WordDictionary wordDictionary = new WordDictionary();
wordDictionary.addWord("bad");
wordDictionary.addWord("dad");
wordDictionary.addWord("mad");
wordDictionary.search("pad"); // return False
wordDictionary.search("bad"); // return True
wordDictionary.search(".ad"); // return True
wordDictionary.search("b.."); // return True
```

## Constraints

- `1 <= word.length <= 25`
- `word` consists of lowercase English letters and dot '.'.
- At most `10^4` calls will be made to addWord and search.

## Solution Approaches

### Approach 1: Trie with DFS for Wildcard
**Time Complexity:** O(m) for addWord, O(26^m) worst case for search with all dots  
**Space Complexity:** O(total_characters)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()
    
    def addWord(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        return self._search_helper(word, 0, self.root)
    
    def _search_helper(self, word, index, node):
        if index == len(word):
            return node.is_end
        
        char = word[index]
        if char == '.':
            for child in node.children.values():
                if self._search_helper(word, index + 1, child):
                    return True
            return False
        else:
            if char not in node.children:
                return False
            return self._search_helper(word, index + 1, node.children[char])
```

### Approach 2: Trie with BFS for Wildcard
**Time Complexity:** O(m) for addWord, O(26^m) worst case for search  
**Space Complexity:** O(total_characters)

```python
from collections import deque

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class WordDictionary:
    def __init__(self):
        self.root = TrieNode()
    
    def addWord(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        queue = deque([self.root])
        
        for char in word:
            size = len(queue)
            for _ in range(size):
                node = queue.popleft()
                if char == '.':
                    queue.extend(node.children.values())
                elif char in node.children:
                    queue.append(node.children[char])
        
        return any(node.is_end for node in queue)
```

### Approach 3: Dictionary by Length
**Time Complexity:** O(1) for addWord, O(n * m) for search  
**Space Complexity:** O(total_characters)

```python
class WordDictionary:
    def __init__(self):
        self.words_by_length = {}
    
    def addWord(self, word):
        length = len(word)
        if length not in self.words_by_length:
            self.words_by_length[length] = []
        self.words_by_length[length].append(word)
    
    def search(self, word):
        length = len(word)
        if length not in self.words_by_length:
            return False
        
        for stored_word in self.words_by_length[length]:
            match = True
            for i, char in enumerate(word):
                if char != '.' and char != stored_word[i]:
                    match = False
                    break
            if match:
                return True
        return False
```

## Key Insights

1. **Wildcard '.'** requires exploring all children
2. **DFS is natural** for recursive search
3. **Group by length** can be simpler for some cases

## Related Problems

- Implement Trie (Prefix Tree) (LeetCode #208)
- Word Search II (LeetCode #212)