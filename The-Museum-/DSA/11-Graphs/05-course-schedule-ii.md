# Course Schedule II

**Difficulty:** Medium  
**Pattern:** Graphs  
**LeetCode:** #210

## Problem Statement

Return the ordering of courses you should take to finish all courses. If impossible, return an empty array.

## Solution Approaches

### Approach 1: BFS Topological Sort
**Time Complexity:** O(V + E)  
**Space Complexity:** O(V + E)

```python
from collections import deque

def findOrder(numCourses, prerequisites):
    graph = [[] for _ in range(numCourses)]
    in_degree = [0] * numCourses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque([i for i in range(numCourses) if in_degree[i] == 0])
    result = []
    
    while queue:
        course = queue.popleft()
        result.append(course)
        for neighbor in graph[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return result if len(result) == numCourses else []
```

### Approach 2: DFS
**Time Complexity:** O(V + E)  
**Space Complexity:** O(V + E)

```python
def findOrder(numCourses, prerequisites):
    graph = [[] for _ in range(numCourses)]
    for course, prereq in prerequisites:
        graph[course].append(prereq)
    
    visited = [0] * numCourses
    result = []
    
    def dfs(course):
        if visited[course] == 1:
            return False
        if visited[course] == 2:
            return True
        
        visited[course] = 1
        for prereq in graph[course]:
            if not dfs(prereq):
                return False
        visited[course] = 2
        result.append(course)
        return True
    
    for course in range(numCourses):
        if not dfs(course):
            return []
    return result
```
