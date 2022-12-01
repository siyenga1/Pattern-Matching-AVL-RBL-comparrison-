class Node:
    def __init__(self, dataIn):
        """
        Constructor for the Node.
        inputs dataIn for the data
        Initialize the node with
        left and right child as None
        """
        self.data = dataIn
        self.left = None
        self.right = None
        self.depth = 1

    def updateDepth(self, depth):
        """
        Updates the depth of the node.
        """
        self.depth = depth

    def __str__(self):
        """
        String representation for the Node
        """
        return "Node value: " + str(self.data)

    def getLeft(self):
        """
        gets the left child of the node
        """
        return self.left

    def getRight(self):
        """
        gets the right child of the node
        """
        return self.right