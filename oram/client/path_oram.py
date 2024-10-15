from oram.client.position_map import PositionMap
from oram.constants import Z_BUCKET_SIZE, N_BLOCKS_NUMBER
from oram.server.bucket_tree import BucketTree


class PathORAM():

    def __init__(self):
        self.n_block_number = N_BLOCKS_NUMBER
        self.z_bucket_size = Z_BUCKET_SIZE
        self.position_map = PositionMap(N_BLOCKS_NUMBER)
        self.bucket_tree = BucketTree(N_BLOCKS_NUMBER)
        self.l_tree_height = self.bucket_tree.height
        self.stash = []

    def access(self, block_id, write=False, new_data=None):
        old_leaf_id = self.position_map.get_leaf_index(block_id)
        old_leaf = self.bucket_tree.get_bucket_by_id(old_leaf_id)
        self.position_map.update_position(block_id)

        # print height of the tree
        print("L Tree Height:", self.l_tree_height)

        for i in range(self.l_tree_height+1):
            bucket = self.bucket_tree.get_bucket_from_path_and_level(old_leaf, i)
            print("1 Bucket:", bucket)
            self.stash.append(bucket.get_block_by_index(block_id))
        # print all stash blocks
        print("Stash:")
        for block in self.stash:
            print(block)
        stash_data = self.stash[block_id]
        if write:
            # update the data in the block
            self.stash[block_id].data = new_data

        temp_stash = []

        # iterate from l_tree_height to 0
        for i in range(self.l_tree_height, 0, -1):
            stash_block = self.stash[-1]
            print("Old leaf:", old_leaf)
            bucket_level_i_old_leaf = self.bucket_tree.get_bucket_from_path_and_level(old_leaf, i)

            print("Stash block:", stash_block)
            stash_block_leaf_id = self.position_map.get_leaf_index(stash_block.id)
            print("Stash block leaf ID:", stash_block_leaf_id)
            stash_block_leaf = self.bucket_tree.get_bucket_by_id(stash_block_leaf_id)
            print("stash_block_leaf:", stash_block_leaf)
            bucket_level_i_stash_block_leaf = self.bucket_tree.get_bucket_from_path_and_level(stash_block_leaf, i)

            if bucket_level_i_old_leaf == bucket_level_i_stash_block_leaf:
                temp_stash.append(stash_block)

            nr_blocks_to_insert = min(self.z_bucket_size, len(temp_stash))
            # store in temp_stash the last nr_blocks_to_insert blocks
            temp_stash = temp_stash[:nr_blocks_to_insert]
            # remove the last nr_blocks_to_insert blocks from stash_copy
            self.stash = self.stash[:-nr_blocks_to_insert]

            # add the last nr_blocks_to_insert blocks to the bucket
            for block in temp_stash:
                bucket_level_i_old_leaf.add_block(block)
            temp_stash = []
        return stash_data

if __name__ == "__main__":
    path_oram = PathORAM()
    print("Path ORAM initialized")
    print("Position Map:")
    path_oram.position_map.print_position_map()
    print("Bucket Tree:")
    path_oram.bucket_tree.print_tree()
    print("Stash:")
    print(path_oram.stash)
    print("Done")

    block_id = 1
    path_oram.access(block_id)
    print("Accessed block with ID", block_id)
    print("Position Map:")
    path_oram.position_map.print_position_map()
    print("Bucket Tree:")
    path_oram.bucket_tree.print_tree()
    print("Stash:")
    print(path_oram.stash)
    print("Done")
