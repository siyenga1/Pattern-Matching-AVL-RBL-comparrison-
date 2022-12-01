import sys


class NodeColor:
    RED = 1
    BLACK = 2

    @staticmethod
    def get_color(color):
        if color == NodeColor.RED:
            return "R"
        else:
            return "B"


"""
    This class represents a single node in red black tree
"""
class TreeNode:
    def __init__(self, node_value):
        self.value = node_value
        self.parent = None
        self.left = None
        self.right = None
        self.color = NodeColor.RED

    def __str__(self):
        if self.value == (-sys.maxsize - 1):
            return 'Node not found'
        else:
            return 'node found in the tree: value: ' + str(self.value) + ', color: ' + NodeColor.get_color(self.color)


class RedBlackTree:
    def __init__(self):
        self.TNULL = TreeNode(-sys.maxsize - 1)
        self.TNULL.color = NodeColor.BLACK
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL
        self.log_level = 1

    # ------ start: helper functions
    def log(self, log_string):
        if self.log_level > 0:
            print(log_string)

    def print_tree(self, current_node, level=1):
        if current_node != self.TNULL:
            self.print_tree(current_node.right, level + 1)
            print(' ' * 12 * level + '----> ' + str(current_node.value) + ', c:' + NodeColor.get_color(
                current_node.color) + ', l:' + str(level))
            self.print_tree(current_node.left, level + 1)
        else:
            if self.log_level > 1:
                print(' ' * 12 * level + '----> NULL Node')

    def minimum(self, current_node):
        while current_node.left != self.TNULL:
            current_node = current_node.left
        return current_node

    def maximum(self, current_node):
        while current_node.right != self.TNULL:
            current_node = current_node.right
        return current_node

    def left_rotate(self, current_node):
        self.log('left rotating - [' + str(current_node.value) + ']')
        c_right_node = current_node.right
        current_node.right = c_right_node.left
        if c_right_node.left != self.TNULL:
            c_right_node.left.parent = current_node

        c_right_node.parent = current_node.parent
        if current_node.parent is None:
            self.root = c_right_node
        elif current_node == current_node.parent.left:
            current_node.parent.left = c_right_node
        else:
            current_node.parent.right = c_right_node
        c_right_node.left = current_node
        current_node.parent = c_right_node

    def right_rotate(self, current_node):
        self.log('right rotating - [' + str(current_node.value) + ']')
        c_left_node = current_node.left
        current_node.left = c_left_node.right
        if c_left_node.right != self.TNULL:
            c_left_node.right.parent = current_node

        c_left_node.parent = current_node.parent
        if current_node.parent is None:
            self.root = c_left_node
        elif current_node == current_node.parent.right:
            current_node.parent.right = c_left_node
        else:
            current_node.parent.left = c_left_node
        c_left_node.right = current_node
        current_node.parent = c_left_node

    # ------ end: helper functions

    # ------ start: searching a node
    # Search the red black tree
    def _search_tree(self, search_node, node_value):
        if search_node == self.TNULL or node_value == search_node.value:
            return search_node

        if node_value < search_node.value:
            return self._search_tree(search_node.left, node_value)

        return self._search_tree(search_node.right, node_value)

    def search_tree(self, node_value):
        self.log('searching for node - [' + str(node_value) + ']')
        return self._search_tree(self.root, node_value)
    # ------ end: searching a node

    # ------ start: deleting a node
    # Balancing the tree after deletion
    def balance_after_delete(self, c_node):
        while c_node != self.root and c_node.color == NodeColor.BLACK:
            if c_node == c_node.parent.left:
                sibling = c_node.parent.right
                if sibling.color == NodeColor.RED:
                    sibling.color = NodeColor.BLACK
                    c_node.parent.color = NodeColor.RED
                    self.left_rotate(c_node.parent)
                    sibling = c_node.parent.right

                if sibling.left.color == NodeColor.BLACK and sibling.right.color == NodeColor.BLACK:
                    sibling.color = NodeColor.RED
                    c_node = c_node.parent
                else:
                    if sibling.right.color == NodeColor.BLACK:
                        sibling.left.color = NodeColor.BLACK
                        sibling.color = NodeColor.RED
                        self.right_rotate(sibling)
                        sibling = c_node.parent.right

                    sibling.color = c_node.parent.color
                    c_node.parent.color = NodeColor.BLACK
                    sibling.right.color = NodeColor.BLACK
                    self.left_rotate(c_node.parent)
                    c_node = self.root
            else:
                sibling = c_node.parent.left
                if sibling.color == NodeColor.RED:
                    sibling.color = NodeColor.BLACK
                    c_node.parent.color = NodeColor.RED
                    self.right_rotate(c_node.parent)
                    sibling = c_node.parent.left

                if sibling.right.color == NodeColor.BLACK and sibling.left.color == NodeColor.BLACK:
                    sibling.color = NodeColor.RED
                    c_node = c_node.parent
                else:
                    if sibling.left.color == NodeColor.BLACK:
                        sibling.right.color = NodeColor.BLACK
                        sibling.color = NodeColor.RED
                        self.left_rotate(sibling)
                        sibling = c_node.parent.left

                    sibling.color = c_node.parent.color
                    c_node.parent.color = NodeColor.BLACK
                    sibling.left.color = NodeColor.BLACK
                    self.right_rotate(c_node.parent)
                    c_node = self.root
        c_node.color = 0

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Node deletion
    def _delete_node(self, current_node, node_value):
        node_to_be_deleted = self.TNULL

        # search the node to be deleted
        while current_node != self.TNULL:
            if current_node.value == node_value:
                node_to_be_deleted = current_node

            if current_node.value <= node_value:
                current_node = current_node.right
            else:
                current_node = current_node.left

        if node_to_be_deleted == self.TNULL:
            print("Cannot find key in the tree")
            return

        y = node_to_be_deleted
        y_original_color = y.color
        if node_to_be_deleted.left == self.TNULL:
            x = node_to_be_deleted.right
            self.transplant(node_to_be_deleted, node_to_be_deleted.right)
        elif node_to_be_deleted.right == self.TNULL:
            x = node_to_be_deleted.left
            self.transplant(node_to_be_deleted, node_to_be_deleted.left)
        else:
            y = self.minimum(node_to_be_deleted.right)
            y_original_color = y.color
            x = y.right
            if y.parent == node_to_be_deleted:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = node_to_be_deleted.right
                y.right.parent = y

            self.transplant(node_to_be_deleted, y)
            y.left = node_to_be_deleted.left
            y.left.parent = y
            y.color = node_to_be_deleted.color
        if y_original_color == NodeColor.BLACK:
            self.balance_after_delete(x)

    def delete_node(self, node_value):
        self.log('deleting node - [' + str(node_value) + ']')
        self._delete_node(self.root, node_value)
    # ------ end: deleting new node

    # ------ start: inserting new node
    # iteratively balance the tree after insertion
    def balance_tree_after_insert(self, current_node):
        while current_node.parent.color == NodeColor.RED:
            # if parent is right child of grandparent
            if current_node.parent == current_node.parent.parent.right:
                uncle = current_node.parent.parent.left
                # if uncle color is RED
                if uncle.color == NodeColor.RED:
                    uncle.color = NodeColor.BLACK
                    current_node.parent.color = NodeColor.BLACK
                    current_node.parent.parent.color = NodeColor.RED
                    current_node = current_node.parent.parent
                # if uncle color is BLACK
                else:
                    if current_node == current_node.parent.left:
                        current_node = current_node.parent
                        self.right_rotate(current_node)
                    current_node.parent.color = NodeColor.BLACK
                    current_node.parent.parent.color = NodeColor.RED
                    self.left_rotate(current_node.parent.parent)
            # if parent is left child of grandparent
            else:
                uncle = current_node.parent.parent.right

                # if uncle color is RED
                if uncle.color == NodeColor.RED:
                    uncle.color = NodeColor.BLACK
                    current_node.parent.color = NodeColor.BLACK
                    current_node.parent.parent.color = NodeColor.RED
                    current_node = current_node.parent.parent
                # if uncle color is RED
                else:
                    if current_node == current_node.parent.right:
                        current_node = current_node.parent
                        self.left_rotate(current_node)
                    current_node.parent.color = NodeColor.BLACK
                    current_node.parent.parent.color = NodeColor.RED
                    self.right_rotate(current_node.parent.parent)

            if current_node == self.root:
                break
        self.root.color = NodeColor.BLACK

    # insert a new node to the red black tree
    def insert(self, node_value):
        self.log('inserting node - [' + str(node_value) + ']')
        new_node = TreeNode(node_value)
        new_node.parent = None
        new_node.value = node_value
        new_node.left = self.TNULL
        new_node.right = self.TNULL
        new_node.color = NodeColor.RED

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if new_node.value < x.value:
                x = x.left
            else:
                x = x.right

        new_node.parent = y
        if y is None:
            self.root = new_node
        elif new_node.value < y.value:
            y.left = new_node
        else:
            y.right = new_node

        if new_node.parent is None:
            new_node.color = NodeColor.BLACK
            return

        if new_node.parent.parent is None:
            return

        self.balance_tree_after_insert(new_node)

    # ------ end: inserting new node


# if __name__ == "__main__":
#     red_black_tree = RedBlackTree()
#     nodes = [8, 18, 5, 15, 17, 25, 40, 80]
#
#     for node in nodes:
#         red_black_tree.insert(node)
#         red_black_tree.print_tree(red_black_tree.root)
#         print('\n\n')
#
#     red_black_tree.print_tree(red_black_tree.root)
#
#     red_black_tree.delete_node(25)
#     red_black_tree.print_tree(red_black_tree.root)
#     node = red_black_tree.search_tree(25)
#     print(str(node))
#
#     red_black_tree.delete_node(15)
#     red_black_tree.print_tree(red_black_tree.root)
#     node = red_black_tree.search_tree(15)
#     print(str(node))
#
#     node = red_black_tree.search_tree(18)
#     print(str(node))
#
#     red_black_tree.delete_node(5)
#     red_black_tree.print_tree(red_black_tree.root)
#
#     red_black_tree.delete_node(8)
#     red_black_tree.print_tree(red_black_tree.root)