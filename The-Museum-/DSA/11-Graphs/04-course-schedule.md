# Course Schedule

**Difficulty:** Medium  
**Pattern:** Graphs  
**LeetCode:** #207

## Problem Statement

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

Return true if you can finish all courses.

## Solution Approaches

### Approach 1: DFS Cycle Detection
**Time Complexity:** O(V + E)  
**Space Complexity:** O(V + E)

```python
def canFinish(numCourses, prerequisites):
    graph = [[] for _ in range(numCourses)]
    for course, prereq in prerequisites:
        graph[course].append(prereq)
    
    visited = [0] * numCourses  # 0: unvisited, 1: visiting, 2: visited
    
    def has_cycle(course):
        if visited[course] == 1:
            return True
        if visited[course] == 2:
            return False
        
        visited[course] = 1
        for prereq in graph[course]:
            if has_cycle(prereq):
                return True
        visited[course] = 2
        return False
    
    for course in range(numCourses):
        if has_cycle(course):
            return False
    return True
```

### Approach 2: BFS Topological Sort (Kahn's Algorithm)
**Time Complexity:** O(V + E)  
**Space Complexity:** O(V + E)

```python
from collections import deque

def canFinish(numCourses, prerequisites):
    graph = [[] for _ in range(numCourses)]
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    count = 0
    
    while queue:
        course = queue.popleft()
        count += 1
        for neighbor in graph[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return count == numCourses
```

## Key Insights

1. **Cycle detection** - if cycle exists, impossible
2. **Topological sort** - process nodes with 0 in-degree
