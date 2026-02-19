# Longest Repeating Character Replacement

**Difficulty:** Medium  
**Pattern:** Sliding Window  
**LeetCode:** #424

## Problem Statement

You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most `k` times.

Return the length of the longest substring containing the same letter you can get after performing the above operations.

## Examples

### Example 1:
```
Input: s = "ABAB", k = 2
Output: 4
Explanation: Replace the two 'A's with two 'B's or vice versa.
```

### Example 2:
```
Input: s = "AABABBA", k = 1
Output: 4
Explanation: Replace the one 'A' in the middle with 'B' and form "AABBBBA".
```

## Constraints

- `1 <= s.length <= 10^5`
- `s` consists of only uppercase English letters.
- `0 <= k <= s.length`

## Solution Approaches

### Approach 1: Sliding Window with Character Count
**Time Complexity:** O(n)  
**Space Complexity:** O(26) = O(1)

```python
def characterReplacement(s, k):
    count = {}
    max_length = 0
    left = 0
    max_count = 0
    
    for right in range(len(s)):
        count[s[right]] = count.get(s[right], 0) + 1
        max_count = max(max_count, count[s[right]])
        
        # Window is valid if (window_size - max_count) <= k
        while (right - left + 1) - max_count > k:
            count[s[left]] -= 1
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Approach 2: Optimized with Max Frequency
**Time Complexity:** O(n)  
**Space Complexity:** O(26) = O(1)

```python
def characterReplacement(s, k):
    count = [0] * 26
    max_length = 0
    left = 0
    max_freq = 0
    
    for right in range(len(s)):
        idx = ord(s[right]) - ord('A')
        count[idx] += 1
        max_freq = max(max_freq, count[idx])
        
        # If window size - max_freq > k, shrink window
        if (right - left + 1) - max_freq > k:
            count[ord(s[left]) - ord('A')] -= 1
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length
```

### Approach 3: Binary Search
**Time Complexity:** O(n log n)  
**Space Complexity:** O(26) = O(1)

```python
def characterReplacement(s, k):
    def canMakeValidWindow(length):
        count = [0] * 26
        for i in range(length):
            count[ord(s[i]) - ord('A')] += 1
        
        if length - max(count) <= k:
            return True
        
        for i in range(length, len(s)):
            count[ord(s[i]) - ord('A')] += 1
            count[ord(s[i - length]) - ord('A')] -= 1
            if length - max(count) <= k:
                return True
        
        return False
    
    left, right = 1, len(s)
    result = 0
    
    while left <= right:
        mid = (left + right) // 2
        if canMakeValidWindow(mid):
            result = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return result
```

## Key Insights

1. **Window is valid** when `window_size - max_frequency <= k`
2. **Track max frequency** of any character in current window
3. **No need to update max_freq** when shrinking - it only affects result when it increases

## Related Problems

- Longest Substring with At Most K Distinct Characters (LeetCode #340)
- Max Consecutive Ones III (LeetCode #1004)