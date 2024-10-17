from array import ArrayType

from oram.constants import N_BLOCKS_NUMBER


class Block:
    used_ids : ArrayType = [False] * N_BLOCKS_NUMBER

    def __init__(self, is_dummy=True, data=None, block_id=None, leaf_id=None):
        if is_dummy:
            self.is_dummy = True
            self.data = []
            self.block_id : int = -1
            self.leaf_id : int = -1
        else:
            self.data = data
            self.is_dummy = False
            # if Block.used_ids[block_id]:
            #     raise ValueError(f"Block id {block_id} is already in use")
            self.block_id : int = block_id
            self.leaf_id : int = leaf_id
            Block.used_ids[block_id] = True

    def __delete__(self, instance):
        Block.used_ids[self.block_id] = False

    def __str__(self):
        return f"Block id {self.block_id}: {self.data}"


if __name__ == "__main__":
    # array of int data
    data = [1, 2, 3, 4, 5]
    block1 = Block(
        is_dummy=True,
        data=data
    )

    block2 = Block(
        is_dummy=True,
        data=data
    )
    print(block1)
    print(block2)

    # array of int data
    data = [1, 2, 3, 4, 5]
    block1 = Block(
        is_dummy=False,
        data=data,
        block_id=1
    )

    block2 = Block(
        is_dummy=False,
        data=data,
        block_id=2
    )
    print(block1)
    print(block2)
