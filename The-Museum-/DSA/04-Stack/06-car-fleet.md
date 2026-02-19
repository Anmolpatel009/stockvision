# Car Fleet

**Difficulty:** Medium  
**Pattern:** Stack  
**LeetCode:** #853

## Problem Statement

There are `n` cars going to the same destination along a one-lane road. The destination is `target` miles away.

You are given two integer array `position` and `speed`, both of length `n`, where `position[i]` is the position of the `i`th car and `speed[i]` is the speed of the `i`th car (in miles per hour).

A car can never pass another car ahead of it, but it can catch up to it and drive bumper to bumper at the same speed. The faster car will slow down to match the slower car's speed. The distance between these two cars is ignored (i.e., they are assumed to have the same position).

A car fleet is some non-empty set of cars driving at the same speed and same position. If a car catches up to a fleet right at the destination point, it will still be considered as one fleet.

Return the number of car fleets that will arrive at the destination.

## Examples

### Example 1:
```
Input: target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]
Output: 3
Explanation:
The cars starting at 10 (speed 2) and 8 (speed 4) become a fleet, meeting each other at 12.
The car starting at 0 (speed 1) does not catch up to any other car, so it is a fleet by itself.
The cars starting at 5 (speed 1) and 3 (speed 3) become a fleet, meeting each other at 6. The fleet moves at speed 1 until it reaches target.
```

### Example 2:
```
Input: target = 10, position = [3], speed = [3]
Output: 1
```

## Constraints

- `n == position.length == speed.length`
- `1 <= n <= 10^5`
- `0 < target <= 10^6`
- `0 <= position[i] < target`
- All the values of position are unique.
- `0 < speed[i] <= 10^6`

## Solution Approaches

### Approach 1: Monotonic Stack
**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

```python
def carFleet(target, position, speed):
    cars = sorted(zip(position, speed), reverse=True)
    stack = []
    
    for pos, spd in cars:
        time = (target - pos) / spd
        if not stack or time > stack[-1]:
            stack.append(time)
    
    return len(stack)
```

### Approach 2: Without Stack
**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

```python
def carFleet(target, position, speed):
    cars = sorted(zip(position, speed), reverse=True)
    
    fleets = 0
    max_time = 0
    
    for pos, spd in cars:
        time = (target - pos) / spd
        if time > max_time:
            fleets += 1
            max_time = time
    
    return fleets
```

### Approach 3: Using Position Array
**Time Complexity:** O(n log n)  
**Space Complexity:** O(n)

```python
def carFleet(target, position, speed):
    n = len(position)
    indices = sorted(range(n), key=lambda i: position[i], reverse=True)
    
    fleets = 0
    prev_time = 0
    
    for i in indices:
        time = (target - position[i]) / speed[i]
        if time > prev_time:
            fleets += 1
            prev_time = time
    
    return fleets
```

## Key Insights

1. **Sort by position** in descending order
2. **Calculate time** to reach target for each car
3. **Fleet forms** when faster car catches slower car ahead

## Related Problems

- Number of Visible People in a Queue (LeetCode #1944)
- Daily Temperatures (LeetCode #739)