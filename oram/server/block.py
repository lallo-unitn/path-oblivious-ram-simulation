class Block:
    _id = 0

    def __init__(self, is_dummy=True, leaf_id = -1, data=None):
        if is_dummy:
            self.is_dummy = True
            self.data = []
            self._leaf_id = -1
            self._id = -1
        else:
            self.data = data
            self._leaf_id = leaf_id
            Block._id += 1

    def __str__(self):
        return f"Leaf {self._leaf_id}: {self.data}"


if __name__ == "__main__":
    # array of int data
    data = [1, 2, 3, 4, 5]
    block = Block(
        leaf_id=1,
        is_dummy=False,
        data=data
    )
    print(block)