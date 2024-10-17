import random
from math import ceil, log2
from typing import Mapping


class PositionMap:
    def __init__(self, n_block_number):
        self.height = ceil(log2(n_block_number))
        self.num_leaves = pow(2, self.height)
        self.position : Mapping[int, int] = {} # block_id -> leaf_index
        self.__initialize_position_map(n_block_number)

    def __initialize_position_map(self, num_blocks):
        # Assign each block a random leaf node index initially
        for block_id in range(0, num_blocks):
            leaf_index = random.randint(0, self.num_leaves - 1)
            self.position[block_id] = leaf_index

    def get_leaf_index(self, block_id):
        return self.position.get(block_id)

    def update_position(self, block_id):
        # Assign a new random leaf index to the block
        new_leaf_index = random.randint(0, self.num_leaves - 1)
        self.position[block_id] = new_leaf_index
        return new_leaf_index

    def print_position_map(self):
        for block_id, leaf_index in self.position.items():
            print(f"Block ID: {block_id}, Leaf Index: {leaf_index}")

    def __str__(self):
        # print all the block ids and their leaf index
        return f"PositionMap: {self.position}"

if __name__ == "__main__":
    position_map = PositionMap(8)
    block_id = 1
    leaf_index = position_map.get_leaf_index(block_id)
    print(f"Block ID: {block_id}, Leaf Index: {leaf_index}")
    position_map.print_position_map()
    new_leaf_index = position_map.update_position(block_id)
    print(f"=====================================")
    print(position_map)
    position_map.print_position_map()