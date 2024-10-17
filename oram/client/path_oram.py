import random as rand
from typing import List, Dict

from tqdm import tqdm
from collections.abc import Mapping
from oram.client.position_map import PositionMap
from oram.constants import Z_BUCKET_SIZE, N_BLOCKS_NUMBER
from oram.server.block import Block
from oram.server.bucket import Bucket
from oram.server.bucket_tree import BucketTree


class PathORAM():

    def __init__(self):
        self.n_block_number = N_BLOCKS_NUMBER
        self.z_bucket_size = Z_BUCKET_SIZE
        self.position_map = PositionMap(N_BLOCKS_NUMBER)
        self.bucket_tree = BucketTree(N_BLOCKS_NUMBER)
        self.l_tree_height = self.bucket_tree.height
        self.stash : Mapping[int, Block] = {}
        self.stash_blocks_paths_to_root : Mapping[int, List[Bucket]] = {}

    def access(self, block_id, isWrite=False, new_data=None):
        block_leaf_id : int = self.__remap_block(block_id)
        self.__read_path_for_block_leaf(block_leaf_id)
        read_block = self.stash.get(block_id)
        if isWrite:
            self.__update_block(block_id, new_data)
        self.__write_path(block_leaf_id)
        return read_block

    def __remap_block(self, block_id):
        block_leaf_id : int = self.position_map.get_leaf_index(block_id)
        self.position_map.update_position(block_id)
        return block_leaf_id

    def __read_path_for_block_leaf(self, block_leaf_id):
        # get leaf from the block leaf id
        bucket : Bucket = self.bucket_tree.leaf_map.get(block_leaf_id)
        # climb tree to the root using for cycle
        for j in range(self.l_tree_height):
            for block in bucket.get_blocks():
                if not block.is_dummy:
                    # add the block to the stash
                    self.stash[block.block_id] = block
            bucket.do_empty()
            if bucket.parent is None:
                break
            bucket = bucket.parent

    def __update_block(self, block_id, new_data):
        # create a new block with the new data
        new_block = Block(is_dummy=False, data=new_data, block_id=block_id)
        # update the block in the stash
        self.stash[block_id] = new_block

    def __write_path(self, block_leaf_id):
        # get leaf node from the block leaf id
        bucket : Bucket = self.bucket_tree.leaf_map.get(block_leaf_id)
        temp_stash: Mapping[int, Block] = {}
        second_temp_stash: Mapping[int, Block] = {}
        # climb the tree to the root
        for j in range(self.l_tree_height, 0, -1):

            # put in temp_stash the blocks that can be written at the level from the stash
            for block_id, block in self.stash.items():
                temp_block_leaf_id = self.position_map.get_leaf_index(block_id)
                if self.__check_path_intersection(bucket, temp_block_leaf_id, j):
                    temp_stash[block_id] = block

            min_size = min(self.z_bucket_size, len(temp_stash))
            # randomly sample the blocks ids if more than the bucket capacity
            sampled_blocks : List[int] = rand.sample(list(temp_stash.keys()), min_size)

            for block_id in sampled_blocks:
                second_temp_stash[block_id] = temp_stash[block_id]

            # write the blocks to the bucket
            self.__write_bucket(bucket, second_temp_stash)
            # remove the blocks from the stash
            temp_stash = {}
            second_temp_stash = {}
            bucket = bucket.parent


    def __check_path_intersection(self, bucket, temp_block_leaf_id, level):
        temp_bucket : Bucket = self.bucket_tree.get_bucket_from_leaf_and_level(temp_block_leaf_id, level)
        return bucket == temp_bucket

    def __write_bucket(self, bucket : Bucket, temp_stash):
        # add the blocks from the temp stash to the bucket
        for block in temp_stash.values():
            try:
                bucket.add_block(block)
            except ValueError:
                break
            # Remove the block from the stash
            self.stash.pop(block.block_id)


if __name__ == "__main__":
    path_oram = PathORAM()

    warmup_access_number = 50_000  # 3 million warm-up accesses
    simulation_access_number = 50_000  # At least 3 million simulation accesses
    total_accesses = warmup_access_number + simulation_access_number

    stash_size_map : List[int] = [0] * (N_BLOCKS_NUMBER + 1)

    # Warm-up phase
    print("Starting warm-up phase...")
    for i in tqdm(range(warmup_access_number), desc="Warming up", unit="iteration"):
        block_id = i % N_BLOCKS_NUMBER
        output_block = path_oram.access(block_id, isWrite=True, new_data=block_id)

    max_stash_size : int = 0
    s : List[int] = [0] * (N_BLOCKS_NUMBER + 1)

    # Simulation phase (Data Collection)
    print("Starting simulation phase...")
    for i in tqdm(range(simulation_access_number), desc="Simulating", unit="iteration"):
        block_id = i % N_BLOCKS_NUMBER
        output_block = path_oram.access(block_id, isWrite=False, new_data=block_id)
        current_stash_size = len(path_oram.stash)
        max_stash_size = max(max_stash_size, current_stash_size)
        # counts the number of accesses with a given stash size
        stash_size_map[current_stash_size] = stash_size_map[current_stash_size] + 1

    # compute s_i
    for i in range(max_stash_size):
        for j in range(i, max_stash_size):
            s[i] = s[i] + stash_size_map[j]

    # Write data to text file
    output_filename = "oram_stash_data.txt"
    with open(output_filename, "w") as f:
        # First line: -1,s
        f.write(f"-1,{simulation_access_number}\n")
        # Subsequent lines: i,s_i
        for i in range(max_stash_size + 1):
            s_i = stash_size_map[i]
            f.write(f"{i},{s_i}\n")

    print(f"Data collection complete. Results written to {output_filename}.")

    # Optionally, print final stash statistics
    print("Final Stash Size:", len(path_oram.stash))
    print("Percentage of blocks in the stash:", len(path_oram.stash) / N_BLOCKS_NUMBER * 100)

