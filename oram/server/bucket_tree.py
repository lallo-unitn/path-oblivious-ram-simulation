from array import ArrayType
from collections import deque
from math import ceil, log2
from typing import List, Mapping

from oram.server.block import Block
from oram.server.bucket import Bucket
from oram.constants import Z_BUCKET_SIZE


class BucketTree():

    def __init__(self, n_block_number):
        if n_block_number <= 0:
            raise ValueError("Bucket size must be greater than 0")
        self.height = ceil(log2(n_block_number))
        self.leaf_map: Mapping[int, Bucket] = {}
        self.root = self.create_tree(self.height)

    def path_to_root(self, node):
        path : List[Bucket] = []
        while node is not None:
            path.append(node)  # Add the current node to the path
            node = node.parent  # Move to the parent node
        return path

    # log(n) time complexity
    def get_bucket_from_leaf_and_level(self, leaf_id, level):
        leaf = self.leaf_map.get(leaf_id)
        # climb up the tree to the level
        node = leaf
        for _ in range(self.height - level):
            if node is None:
                raise ValueError(f"Level {level} not found")
            node = node.parent
        return node


    def create_tree(self, height, z_max_size=Z_BUCKET_SIZE, parent=None):
        self.root = self.create_tree_wrapped(self.height, z_max_size, parent)
        self.__assign_ids_inverted_bfs()
        return self.root

    def create_tree_wrapped(self, height, z_max_size=Z_BUCKET_SIZE, parent=None):
        if height < 0:
            return None
        node = Bucket(max_size=z_max_size)
        for i in range(z_max_size):
            new_dummy_block = Block(is_dummy=True)
            node.add_block(new_dummy_block)

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
            if node.is_leaf():
                self.leaf_map[node._id] = node

    def is_on_path(self, block_leaf_id, path_leaf_id, level):
        # Calculate the number of bits to shift
        shift_amount = self.height - level

        # Shift both IDs to compare the prefixes
        block_prefix = block_leaf_id >> shift_amount
        path_prefix = path_leaf_id >> shift_amount

        # Check if the prefixes match
        return block_prefix == path_prefix


if __name__ == "__main__":
    bucket_tree = BucketTree(8)
    bucket_tree.print_tree()
    print(f"Tree Height: {bucket_tree.height}")
    bucket_from_leaf_and_level = bucket_tree.get_bucket_from_leaf_and_level(0, 0)
    print(bucket_from_leaf_and_level)

