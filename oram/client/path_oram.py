from oram.client.position_map import PositionMap
from oram.constants import Z_BUCKET_SIZE, N_BLOCKS_NUMBER
from oram.server.bucket_tree import BucketTree


class PathORAM():

    def __init__(self):
        self.n_block_number = N_BLOCKS_NUMBER
        self.z_bucket_size = Z_BUCKET_SIZE
        self.position_map = PositionMap(N_BLOCKS_NUMBER)
        self.bucket_tree = BucketTree(N_BLOCKS_NUMBER)
        self.stash = []


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
