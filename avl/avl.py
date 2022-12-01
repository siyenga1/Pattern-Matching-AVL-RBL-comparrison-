from avl.node import Node


class AVLTree:
    """
    Adelson-Velsky and Landis Tree Implementation
    Initiatize with no parameter to constructor.
    """

    def __init__(self):
        self.root = None

    def search(self, key):
        """
        search function:
        takes in key value and calls internal searchUtil()
        returns parent and node if found. Parent is None
        if key is the root.
        """
        return self.searchUtil(self.root, None, key)

    def searchUtil(self, root, parent, key):
        """
        Searched the tree recursively using the
        same technique as searching in BST
        returns parent node and node containing key
        """
        if not root:
            return None, None
        if root.data == key:
            return parent, root
        elif root.data > key:
            return self.searchUtil(root.left, root, key)
        else:
            return self.searchUtil(root.right, root, key)

    def successorNode(self, root):
        """
        Successor of a node is the next greatest value
        in the Inorder traversal of the tree. It is an
        utility function which removing a node.
        """
        if not root: return root
        while root.left is not None:
            root = root.left
        return root

    def getDepth(self, root):
        """
        Depth of the node. Root node is at 0.
        """
        if not root:
            return 0
        return root.depth

    def updateDepth(self, root):
        """
        Updating depth of nodes when an insert, delete
        or rebalance happens.
        """
        root.updateDepth(1 + max(self.getDepth(root.left), self.getDepth(root.right)))

    def getBalance(self, root):
        """
        Balance Factor of a node.
        """
        return self.getDepth(root.left) - self.getDepth(root.right) if root else 0

    def insert(self, key):
        """
        Inserts a key into a tree using insertUtil.
        If key exists already, returns with a message
        to user. Otherwise adds the key to the tree.
        """
        if self.search(key)[1]:
            print("Cannot Insert Duplicate Key. Please try again with another key!")
            return
        if not self.root:
            self.root = Node(key)
        else:
            self.root = self.insertUtil(self.root, key)
        print("Insert Completed")

    def insertUtil(self, root, key):
        """
        Inserts the key recursively using BST rules.
        After the update, the depth of the subtree where
        the key is inserted is updated and balance factor
        is checked.
        """
        if root is None:
            return Node(key)
        elif root.data < key:
            root.right = self.insertUtil(root.right, key)
        else:
            root.left = self.insertUtil(root.left, key)

        self.updateDepth(root)

        root = self.balancePostInsert(root, key)
        return root

    def balancePostInsert(self, root, key):
        """
        Rebalances the tree as per four rotation
        rules:

        1. LL - Single Rotation
        2. RR - Single Rotation
        3. LR - Double Rotation
        4. RL - Double Rotation

        Depending upon the balance factor of the parent
        and grandparent, these rotations are applied and
        tree is balanced.
        """
        balance = self.getBalance(root)
        if balance < -1:
            if key > root.right.data:
                root = self.leftRotate(root)
            elif key < root.right.data:
                root = self.rightLeftRotate(root)
        elif balance > 1:
            if key < root.left.data:
                root = self.rightRotate(root)
            elif key > root.left.data:
                root = self.leftRightRotate(root)
        return root

    def delete(self, key):
        """
        Search for key in tree. If not found, return
        with a message to user. Otherwise calls
        deleteUtil() to remove the key from the tree
        """
        if not self.search(key)[1]:
            print("Key not Found! Please try again with another key!")
            return
        self.root = self.deleteUtil(self.root, key)
        print("Delete Completed")

    def deleteUtil(self, root, key):
        """
        Delete the key recursively as per rules defined
        for removal in BST.

        BST removal cases:
        1. no right child, replace the node with left child
        2. no left child, replace the node with right child
        3. have both child: find the successor and replace with
            it. Uses internal method successorNode(). BST
            successor nodes are found in the right child of the
            node.
        """
        if root is None:
            return root
        elif root.data > key:
            root.left = self.deleteUtil(root.left, key)
        elif root.data < key:
            root.right = self.deleteUtil(root.right, key)
        else:
            if not root.right:
                left_child = root.left
                root = None
                return left_child
            elif not root.left:
                right_child = root.right
                root = None
                return right_child
            else:
                successor = self.successorNode(root.right)
                root.data = successor.data
                root.right = self.deleteUtil(root.right, successor.data)

        if not root: return root

        self.updateDepth(root)
        root = self.balancePostDelete(root)
        return root

    def balancePostDelete(self, root):
        """
        After removal, update the depth of the subtrees.
        get the Balance Factor of the parent and child
        and as per the four cases, rotate. In removal, we
        might need to balance entire path from root to the
        node.
        """
        balance_parent = self.getBalance(root)

        if balance_parent > 1:
            balance_child = self.getBalance(root.left)
            if balance_child >= 0:
                root = self.rightRotate(root)
            else:
                root = self.leftRightRotate(root)
        elif balance_parent < -1:
            balance_child = self.getBalance(root.right)
            if balance_child <= 0:
                root = self.leftRotate(root)
            else:
                root = self.rightLeftRotate(root)
        return root

    def rightRotate(self, root):
        """
        Rotates the tree with parent as new root,
        grandparent as right child of the
        new root and parent's right child as
        left child of the grandparent.
        """
        newRoot = root.left
        root.left = newRoot.right
        newRoot.right = root

        self.updateDepth(root)
        self.updateDepth(newRoot)
        return newRoot

    def leftRotate(self, root):
        """
        Rotates the tree with parent as new root,
        grandparent as new left child of the
        parent(new root). While the old left
        child of the parent becomes the right child
        of the grandparent.
        """
        newRoot = root.right
        root.right = newRoot.left
        newRoot.left = root

        self.updateDepth(root)
        self.updateDepth(newRoot)
        return newRoot

    def leftRightRotate(self, root):
        """
        Double rotations. First rotate the left
        child of the grandparent with left rotation
        defined above and then do a right rotation
        """
        root.left = self.leftRotate(root.left)
        return self.rightRotate(root)

    def rightLeftRotate(self, root):
        """
        Double rotations. First rotate the right
        child of the grandparent with right rotation
        defined above and then do a left rotation
        on the grandparent.
        """
        root.right = self.rightRotate(root.right)
        return self.leftRotate(root)

    def printInOrder(self):
        """
        Printing Inorder representation of the
        tree using recursion.
        """
        print("Inorder Representation: ")
        self.printInOrderUtil(self.root)
        print()

    def printInOrderUtil(self, root):
        """
        Printing Inorder representation of the
        tree using recursion.
        """
        if root:
            self.printInOrderUtil(root.left)
            print(root.data, end=" ")
            self.printInOrderUtil(root.right)

    def printPreOrder(self):
        """
        Printing Preorder representation of the
        tree using recursion.
        """
        print("PreOrder Representation: ")
        self.printPreOrderUtil(self.root)
        print()

    def printPreOrderUtil(self, root):
        """
        Printing Preorder representation of the
        tree using recursion.
        """
        if root:
            print(root.data, end=" ")
            self.printPreOrderUtil(root.left)
            self.printPreOrderUtil(root.right)

    def printPostOrder(self):
        """
        Printing Postorder representation of the
        tree using recursion.
        """
        print("Postorder Representation: ")
        self.printPostOrderUtil(self.root)
        print()

    def printPostOrderUtil(self, root):
        """
        Printing Postorder representation of the
        tree using recursion.
        """
        if root:
            self.printPostOrderUtil(root.left)
            self.printPostOrderUtil(root.right)
            print(root.data, end=" ")

    def printTree(self):
        """
        Printing visual representation of the
        tree using recursion. Prints tree
        horizontally, with root as the left most.
        tree grows right with right child above and
        left child down.

        example: root a with left child b and right
        child c will print as
                ----> c
        ----> a
                ----> b
        """
        print("Pretty Print Tree")
        self.printTreeUtil(self.root)

    def printTreeUtil(self, node, level=0):
        """
        Printing visual representation of the
        tree using recursion.
        """
        if node:
            self.printTreeUtil(node.right, level + 1)
            print(' ' * 8 * level + '----> ' + str(node.data))
            self.printTreeUtil(node.left, level + 1)