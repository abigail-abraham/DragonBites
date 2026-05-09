class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.data = None  # Store associated data (e.g., restaurant ID)


class Trie:
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word, data=None):
        word = word.lower().strip()
        node = self.root
        
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.data = data
    
    def search(self, word):
        word = word.lower().strip()
        node = self.root
        
        for char in word:
            if char not in node.children:
                return False, None
            node = node.children[char]
        
        return node.is_end_of_word, node.data
    
    def autocomplete(self, prefix, limit=10):
        
        prefix = prefix.lower().strip()
        node = self.root
        results = []
        
        # Navigate to the end of prefix
        for char in prefix:
            if char not in node.children:
                return results
            node = node.children[char]
        
        # DFS to find all words with this prefix
        self._dfs(node, prefix, results, limit)
        return results
    
    def _dfs(self, node, current_word, results, limit):
        if len(results) >= limit:
            return
        
        if node.is_end_of_word:
            results.append((current_word, node.data))
        
        for char, child_node in sorted(node.children.items()):
            if len(results) >= limit:
                break
            self._dfs(child_node, current_word + char, results, limit)
    
    def starts_with(self, prefix):
        prefix = prefix.lower().strip()
        node = self.root
        
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        
        return True
    
    def delete(self, word):
        """
        Delete a word from the trie
        
        Returns: True if word was deleted, False if not found
        """
        word = word.lower().strip()
        
        def _delete_helper(node, word, index):
            if index == len(word):
                if not node.is_end_of_word:
                    return False
                node.is_end_of_word = False
                node.data = None
                return len(node.children) == 0
            
            char = word[index]
            if char not in node.children:
                return False
            
            child_node = node.children[char]
            should_delete_child = _delete_helper(child_node, word, index + 1)
            
            if should_delete_child:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end_of_word
            
            return False
        
        return _delete_helper(self.root, word, 0)
