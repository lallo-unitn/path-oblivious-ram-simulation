from collections import deque
from math import ceil, log2

from oram.server.block import Block
from oram.server.bucket import Bucket
from oram.constants import Z_BUCKET_SIZE


class BucketTree():

    def __init__(self, n_block_number):
        if n_block_number <= 0:
            raise ValueError("Bucket size must be greater than 0")
        self.height = ceil(log2(n_block_number))
        self.root = self.create_tree(self.height)

    def path_to_root(self, node):
        path = []
        while node is not None:
            path.append(node)  # Add the current node to the path
            node = node.parent  # Move to the parent node
        return path

    def get_bucket_from_path_and_level(self, node, level):
        path = self.path_to_root(node)
        if level < 0 or level > len(path):
            raise ValueError("Level out of bounds")
        return path[len(path) - 1 - level]

    def create_tree(self, height, z_max_size=Z_BUCKET_SIZE, parent=None):
        self.root = self.create_tree_wrapped(self.height, z_max_size, parent)
        self.__assign_ids_inverted_bfs()
        return self.root

    def create_tree_wrapped(self, height, z_max_size=Z_BUCKET_SIZE, parent=None):
        if height < 0:
            return None
        node = Bucket(max_size=z_max_size)
        for _ in range(z_max_size):
            node.add_block(Block(is_dummy=True))
        node.left = self.create_tree_wrapped(
            height=height - 1,
            z_max_size=z_max_size,
            parent=node
        )
        node.right = self.create_tree_wrapped(
            height=height - 1,
            z_max_size=z_max_size,
            parent=node
        )
        if node.left is not None:
            node.left.parent = node
        if node.right is not None:
            node.right.parent = node
        return node

    def print_tree(self, node=None, level=0, prefix="Root: "):
        if node is None:
            node = self.root
        # Print the current node with indentation
        print("    " * level + prefix + str(node))
        # print block of the node
        for block in node.get_blocks():
            print("    " * (level) + str(block))
        # Recursively print the left and right subtrees
        if node.left is not None:
            self.print_tree(node.left, level + 1, prefix="L--- ")
        if node.right is not None:
            self.print_tree(node.right, level + 1, prefix="R--- ")

    def get_bucket_by_id(self, bucket_id):
        return self.get_bucket_by_id_wrapped(self.root, bucket_id)

    def get_bucket_by_id_wrapped(self, node, bucket_id):
        if node is None:
            return None
        if node._id == bucket_id:
            return node
        left = self.get_bucket_by_id_wrapped(node.left, bucket_id)
        if left is not None:
            return left
        right = self.get_bucket_by_id_wrapped(node.right, bucket_id)
        if right is not None:
            return right
        return None

    def __assign_ids_inverted_bfs(self):
        if not self.root:
            return

        # Perform a BFS traversal and collect nodes in a list
        queue = deque([self.root])
        nodes = []

        while queue:
            node = queue.popleft()
            nodes.append(node)

            # Add children to the queue for BFS
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        # Reverse the list for inverted BFS order
        nodes.reverse()

        # Assign IDs in reverse BFS order, starting from 0
        for i, node in enumerate(nodes):
            node._id = i  # Start IDs from 0

if __name__ == "__main__":
    bucket_tree = BucketTree(8)
    bucket_tree.print_tree()

