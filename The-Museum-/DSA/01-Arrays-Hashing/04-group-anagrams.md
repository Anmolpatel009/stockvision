# Group Anagrams

**Difficulty:** Medium  
**Pattern:** Arrays & Hashing  
**LeetCode:** #49

## Problem Statement

Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

## Examples

### Example 1:
```
Input: strs = ["eat","tea","tan","ate","nat","bat"]
Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
```

### Example 2:
```
Input: strs = [""]
Output: [[""]]
```

### Example 3:
```
Input: strs = ["a"]
Output: [["a"]]
```

## Constraints

- `1 <= strs.length <= 10^4`
- `0 <= strs[i].length <= 100`
- `strs[i]` consists of lowercase English letters.

## Solution Approaches

### Approach 1: Sort Each String
**Time Complexity:** O(n * k log k) where k is max string length  
**Space Complexity:** O(n * k)

```python
from collections import defaultdict

def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        sorted_str = ''.join(sorted(s))
        groups[sorted_str].append(s)
    return list(groups.values())
```

### Approach 2: Character Count as Key
**Time Complexity:** O(n * k)  
**Space Complexity:** O(n * k)

```python
from collections import defaultdict

def groupAnagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        key = tuple(count)
        groups[key].append(s)
    return list(groups.values())
```

### Approach 3: Prime Number Hash
**Time Complexity:** O(n * k)  
**Space Complexity:** O(n * k)

```python
from collections import defaultdict

def groupAnagrams(strs):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 
              43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    
    groups = defaultdict(list)
    for s in strs:
        key = 1
        for c in s:
            key *= primes[ord(c) - ord('a')]
        groups[key].append(s)
    return list(groups.values())
```

## Key Insights

1. **Sorting approach** is simplest and most intuitive
2. **Character count** avoids sorting overhead for longer strings
3. **Prime multiplication** provides unique hash but may overflow for very long strings

## Related Problems

- Valid Anagram (LeetCode #242)
- Find All Anagrams in a String (LeetCode #438)
