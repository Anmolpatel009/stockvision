# Permutation in String

**Difficulty:** Medium  
**Pattern:** Sliding Window  
**LeetCode:** #567

## Problem Statement

Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`, or `false` otherwise.

In other words, return `true` if one of `s1`'s permutations is the substring of `s2`.

## Examples

### Example 1:
```
Input: s1 = "ab", s2 = "eidbaooo"
Output: true
Explanation: s2 contains one permutation of s1 ("ba").
```

### Example 2:
```
Input: s1 = "ab", s2 = "eidboaoo"
Output: false
```

## Constraints

- `1 <= s1.length, s2.length <= 10^4`
- `s1` and `s2` consist of lowercase English letters.

## Solution Approaches

### Approach 1: Sliding Window with Character Count
**Time Complexity:** O(n)  
**Space Complexity:** O(26) = O(1)

```python
def checkInclusion(s1, s2):
    if len(s1) > len(s2):
        return False
    
    s1_count = [0] * 26
    s2_count = [0] * 26
    
    for i in range(len(s1)):
        s1_count[ord(s1[i]) - ord('a')] += 1
        s2_count[ord(s2[i]) - ord('a')] += 1
    
    matches = 0
    for i in range(26):
        if s1_count[i] == s2_count[i]:
            matches += 1
    
    left = 0
    for right in range(len(s1), len(s2)):
        if matches == 26:
            return True
        
        index = ord(s2[right]) - ord('a')
        s2_count[index] += 1
        if s2_count[index] == s1_count[index]:
            matches += 1
        elif s2_count[index] == s1_count[index] + 1:
            matches -= 1
        
        index = ord(s2[left]) - ord('a')
        s2_count[index] -= 1
        if s2_count[index] == s1_count[index]:
            matches += 1
        elif s2_count[index] == s1_count[index] - 1:
            matches -= 1
        
        left += 1
    
    return matches == 26
```

### Approach 2: Sliding Window with Hash Map
**Time Complexity:** O(n)  
**Space Complexity:** O(26) = O(1)

```python
from collections import Counter

def checkInclusion(s1, s2):
    s1_count = Counter(s1)
    window_count = Counter()
    left = 0
    
    for right, char in enumerate(s2):
        window_count[char] += 1
        
        if right - left + 1 > len(s1):
            window_count[s2[left]] -= 1
            if window_count[s2[left]] == 0:
                del window_count[s2[left]]
            left += 1
        
        if window_count == s1_count:
            return True
    
    return False
```

### Approach 3: Sorted String Comparison
**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

```python
def checkInclusion(s1, s2):
    sorted_s1 = sorted(s1)
    
    for i in range(len(s2) - len(s1) + 1):
        if sorted(s2[i:i + len(s1)]) == sorted_s1:
            return True
    
    return False
```

## Key Insights

1. **Fixed window size** = length of s1
2. **Compare character counts** instead of actual permutations
3. **Track matches** for O(1) comparison

## Related Problems

- Find All Anagrams in a String (LeetCode #438)
- Minimum Window Substring (LeetCode #76)