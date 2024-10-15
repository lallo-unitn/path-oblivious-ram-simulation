from oram.server.block import Block


class Stash():

    def __init__(self):
        self.__blocks = []

    def add_block(self, block):
        if not isinstance(block, Block):
            raise ValueError("Block must be of type Block")
        self.__blocks.append(block)
