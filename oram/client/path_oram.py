import random as rand
import matplotlib.pyplot as plt
import numpy as np
from typing import List
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

    warmup_access_number = 100_000  # 3 million warm-up accesses
    simulation_access_number = 100_000  # At least 3 million simulation accesses
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

    # ... [Your existing code up to data collection] ...

    # Compute s_i (the cumulative counts of stash sizes ≥ i)
    s = [0] * (max_stash_size + 1)
    for i in range(max_stash_size + 1):
        s[i] = sum(stash_size_map[i:])

    # Write data to text file
    output_filename = "oram_stash_data.txt"
    with open(output_filename, "w") as f:
        # First line: -1, total number of simulation accesses
        f.write(f"-1,{simulation_access_number}\n")
        # Subsequent lines: i, s_i
        for i in range(max_stash_size + 1):
            f.write(f"{i},{s[i]}\n")

    print(f"Data collection complete. Results written to {output_filename}.")

    # Compute probabilities (excluding the stash size of 0)
    prob = [(s_i / simulation_access_number) * 100 for s_i in s[1:]]

    # Create the range for the X-axis (from 1 to max_stash_size)
    x_values = np.arange(1, max_stash_size + 1)

    # Create bar plot with specified probabilities
    bars = plt.bar(x_values, prob, color='blue', edgecolor='black')

    # Set x-axis ticks to be integers
    plt.xticks(x_values)

    # Add percentage labels on top of each bar
    for bar, percentage in zip(bars, prob):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.5,  # Adjust the position slightly above the bar
            f'{percentage:.2f}%',
            ha='center',
            va='bottom',
            fontsize=8
        )

    # Add title and labels
    plt.title(f'PORAM Simulation for Z={Z_BUCKET_SIZE}')
    plt.xlabel('Required Stash Size')
    plt.ylabel('P[Stash Size ≥ Required Stash Size] (%)')

    # Adjust layout to prevent clipping of ylabel
    plt.tight_layout()

    # Save the histogram as an image
    plt.savefig('histogram_image.png')

    # Show the plot
    plt.show()

    # Optionally, print final stash statistics
    print("Final Stash Size:", len(path_oram.stash))
    print("Percentage of blocks in the stash:", len(path_oram.stash) / N_BLOCKS_NUMBER * 100)
