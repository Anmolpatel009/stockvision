# Valid Sudoku

**Difficulty:** Medium  
**Pattern:** Arrays & Hashing  
**LeetCode:** #36

## Problem Statement

Determine if a `9 x 9` Sudoku board is valid. Only the filled cells need to be validated according to the following rules:

1. Each row must contain the digits `1-9` without repetition.
2. Each column must contain the digits `1-9` without repetition.
3. Each of the nine `3 x 3` sub-boxes of the grid must contain the digits `1-9` without repetition.

## Examples

### Example 1:
```
Input: board = 
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: true
```

### Example 2:
```
Input: board = 
[["8","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
Output: false
Explanation: Same as Example 1, except with the 5 in the top left corner being modified to 8. Since there are two 8's in the top left 3x3 sub-box, it is invalid.
```

## Constraints

- `board.length == 9`
- `board[i].length == 9`
- `board[i][j]` is a digit `1-9` or `'.'`.

## Solution Approaches

### Approach 1: Hash Sets for Rows, Columns, and Boxes
**Time Complexity:** O(9²) = O(1)  
**Space Complexity:** O(9²) = O(1)

```python
def isValidSudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    
    for r in range(9):
        for c in range(9):
            if board[r][c] == '.':
                continue
            
            num = board[r][c]
            box_idx = (r // 3) * 3 + (c // 3)
            
            if num in rows[r] or num in cols[c] or num in boxes[box_idx]:
                return False
            
            rows[r].add(num)
            cols[c].add(num)
            boxes[box_idx].add(num)
    
    return True
```

### Approach 2: Single Pass with String Encoding
**Time Complexity:** O(9²) = O(1)  
**Space Complexity:** O(9²) = O(1)

```python
def isValidSudoku(board):
    seen = set()
    
    for r in range(9):
        for c in range(9):
            if board[r][c] == '.':
                continue
            
            num = board[r][c]
            row_key = f"{num} in row {r}"
            col_key = f"{num} in col {c}"
            box_key = f"{num} in box {r//3}-{c//3}"
            
            if row_key in seen or col_key in seen or box_key in seen:
                return False
            
            seen.add(row_key)
            seen.add(col_key)
            seen.add(box_key)
    
    return True
```

### Approach 3: Bitmask
**Time Complexity:** O(9²) = O(1)  
**Space Complexity:** O(9) = O(1)

```python
def isValidSudoku(board):
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    
    for r in range(9):
        for c in range(9):
            if board[r][c] == '.':
                continue
            
            num = int(board[r][c])
            bit = 1 << num
            box_idx = (r // 3) * 3 + (c // 3)
            
            if rows[r] & bit or cols[c] & bit or boxes[box_idx] & bit:
                return False
            
            rows[r] |= bit
            cols[c] |= bit
            boxes[box_idx] |= bit
    
    return True
```

## Key Insights

1. **Box index formula**: `(row // 3) * 3 + (col // 3)`
2. **Bitmask** is most space-efficient
3. All approaches are O(1) since board size is fixed

## Related Problems

- Sudoku Solver (LeetCode #37)
