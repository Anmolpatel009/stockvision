# Design Twitter

**Difficulty:** Medium  
**Pattern:** Heap / Priority Queue  
**LeetCode:** #355

## Problem Statement

Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and see the 10 most recent tweets in the user's news feed.

Implement the `Twitter` class:
- `Twitter()` Initializes your twitter object.
- `void postTweet(int userId, int tweetId)` Composes a new tweet with ID tweetId by the user userId.
- `List<Integer> getNewsFeed(int userId)` Retrieves the 10 most recent tweet IDs in the user's news feed.
- `void follow(int followerId, int followeeId)` The user with ID followerId started following the user with ID followeeId.
- `void unfollow(int followerId, int followeeId)` The user with ID followerId started unfollowing the user with ID followeeId.

## Examples

### Example 1:
```
Input
["Twitter", "postTweet", "getNewsFeed", "follow", "postTweet", "getNewsFeed", "unfollow", "getNewsFeed"]
[[], [1, 5], [1], [1, 2], [2, 6], [1], [1, 2], [1]]
Output
[null, null, [5], null, null, [6, 5], null, [5]]
```

## Constraints

- `1 <= userId, followerId, followeeId <= 500`
- `0 <= tweetId <= 10^4`
- All the tweets have unique IDs.
- At most `3 * 10^4` calls will be made to postTweet, getNewsFeed, follow, and unfollow.

## Solution Approaches

### Approach 1: Heap with Timestamp
**Time Complexity:** O(n log n) for getNewsFeed  
**Space Complexity:** O(total_tweets + total_follows)

```python
import heapq
from collections import defaultdict, deque

class Twitter:
    def __init__(self):
        self.timestamp = 0
        self.tweets = defaultdict(deque)  # userId -> deque of (timestamp, tweetId)
        self.following = defaultdict(set)  # userId -> set of followeeId
    
    def postTweet(self, userId, tweetId):
        self.tweets[userId].appendleft((self.timestamp, tweetId))
        self.timestamp += 1
        
        # Keep only recent 10 tweets
        if len(self.tweets[userId]) > 10:
            self.tweets[userId].pop()
    
    def getNewsFeed(self, userId):
        heap = []
        
        # Get tweets from self and all followees
        users = self.following[userId] | {userId}
        
        for user in users:
            for timestamp, tweetId in self.tweets[user]:
                heapq.heappush(heap, (timestamp, tweetId))
                if len(heap) > 10:
                    heapq.heappop(heap)
        
        return [tweetId for _, tweetId in sorted(heap, reverse=True)]
    
    def follow(self, followerId, followeeId):
        self.following[followerId].add(followeeId)
    
    def unfollow(self, followerId, followeeId):
        self.following[followerId].discard(followeeId)
```

### Approach 2: Merge K Sorted Lists
**Time Complexity:** O(10 * log(followees)) for getNewsFeed  
**Space Complexity:** O(total_tweets + total_follows)

```python
import heapq
from collections import defaultdict, deque

class Twitter:
    def __init__(self):
        self.timestamp = 0
        self.tweets = defaultdict(deque)
        self.following = defaultdict(set)
    
    def postTweet(self, userId, tweetId):
        self.tweets[userId].appendleft((self.timestamp, tweetId))
        self.timestamp += 1
        if len(self.tweets[userId]) > 10:
            self.tweets[userId].pop()
    
    def getNewsFeed(self, userId):
        heap = []
        users = self.following[userId] | {userId}
        
        # Initialize heap with most recent tweet from each user
        for user in users:
            if self.tweets[user]:
                timestamp, tweetId = self.tweets[user][0]
                heapq.heappush(heap, (-timestamp, user, 0, tweetId))
        
        result = []
        while heap and len(result) < 10:
            neg_ts, user, idx, tweetId = heapq.heappop(heap)
            result.append(tweetId)
            
            if idx + 1 < len(self.tweets[user]):
                next_ts, next_tweet = self.tweets[user][idx + 1]
                heapq.heappush(heap, (-next_ts, user, idx + 1, next_tweet))
        
        return result
    
    def follow(self, followerId, followeeId):
        self.following[followerId].add(followeeId)
    
    def unfollow(self, followerId, followeeId):
        self.following[followerId].discard(followeeId)
```

## Key Insights

1. **Store tweets with timestamps** for ordering
2. **Merge k sorted lists** approach for efficient feed retrieval
3. **Limit stored tweets** per user to optimize space

## Related Problems

- Merge k Sorted Lists (LeetCode #23)
- Design HashSet (LeetCode #705)