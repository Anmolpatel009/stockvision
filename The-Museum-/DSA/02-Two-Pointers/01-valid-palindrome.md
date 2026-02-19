# Valid Palindrome

**Difficulty:** Easy  
**Pattern:** Two Pointers  
**LeetCode:** #125

## Problem Statement

A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.

Given a string `s`, return `true` if it is a palindrome, or `false` otherwise.

## Examples

### Example 1:
```
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.
```

### Example 2:
```
Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.
```

### Example 3:
```
Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
```

## Constraints

- `1 <= s.length <= 2 * 10^5`
- `s` consists only of printable ASCII characters.

## Solution Approaches

### Approach 1: Two Pointers
**Time Complexity:** O(n)  
**Space Complexity:** O(1)

```python
def isPalindrome(s):
    left, right = 0, len(s) - 1
    
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True
```

### Approach 2: Build Clean String and Check
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def isPalindrome(s):
    clean = ''.join(c.lower() for c in s if c.isalnum())
    return clean == clean[::-1]
```

### Approach 3: Two Pointers with Preprocessing
**Time Complexity:** O(n)  
**Space Complexity:** O(n)

```python
def isPalindrome(s):
    clean = [c.lower() for c in s if c.isalnum()]
    left, right = 0, len(clean) - 1
    
    while left < right:
        if clean[left] != clean[right]:
            return False
        left += 1
        right -= 1
    
    return True
```

## Key Insights

1. **Two pointers** from both ends is most space-efficient
2. **Skip non-alphanumeric** characters in place
3. **Case-insensitive** comparison using `.lower()`

## Related Problems

- Valid Palindrome II (LeetCode #680)
- Palindrome Number (LeetCode #9)