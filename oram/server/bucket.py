from oram.server.block import Block

class Bucket():

    def __init__(self, max_size=0, parent=None, right=None, left=None, blocks=None):
        if blocks is None:
            blocks = []
        self.__is_init = False
        if max_size <= 0:
            raise ValueError("Bucket size must be greater than 0")
        self.is_init = True
        self.parent = parent
        self.right = right
        self.left = left
        self.__max_size = max_size
        self.__blocks = blocks

    def get_block_by_index(self, index):
        if index < 0 or index >= len(self.__blocks):
            raise ValueError("Index out of bounds")
        return self.__blocks[index]

    def add_block(self, block):
        if len(self.__blocks) >= self.__max_size:
            raise ValueError("Bucket is full")
        if not isinstance(block, Block):
            raise ValueError("Block must be of type Block")
        self.__blocks.append(block)

    def get_blocks(self):
        return self.__blocks

    def remove_block(self, index):
        if index < 0 or index >= len(self.__blocks):
            raise ValueError("Index out of bounds")
        self.__blocks.pop(index)

    def get_max_size(self):
        return self.__max_size

    def set_max_size(self, max_size):
        if self.__is_init:
            raise ValueError("Bucket is already initialized")
        if max_size <= 0:
            raise ValueError("Bucket size must be greater than 0")
        self.__max_size = max_size
        self.__is_init = True

    def reset_state(self):
        self.__is_init = False

    def __str__(self):
        return f"Bucket(max_size={self.__max_size}, blocks={len(self.__blocks)})"


if __name__ == "__main__":
    # Create a bucket with max size 5
    bucket = Bucket(5)

    # Create a block with data [1, 2, 3, 4, 5]
    data = [1, 2, 3, 4, 5]
    block = Block(0, 0, data)

    # create second block
    data2 = [6, 7, 8, 9, 10]
    block2 = Block(1, 1, data2)

    # Add the block to the bucket
    bucket.add_block(block)
    bucket.add_block(block2)

    # Get the block by index
    blocks = bucket.get_blocks()
    for block in blocks:
        print(block)

    # Remove the block
    bucket.remove_block(0)

    # Reset the state of the bucket
    bucket.reset_state()