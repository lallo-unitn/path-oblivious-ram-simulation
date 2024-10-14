class Block:

    def __init__(self, leaf_id=-1, index=-1, data=None):
        self.leaf_id = leaf_id
        self.index = index
        self.data = data

    def __str__(self):
        return f"Leaf {self.leaf_id}: {self.data}"


if __name__ == "__main__":
    # array of int data
    data = [1, 2, 3, 4, 5]
    block = Block(0, 0, data)
    print(block)