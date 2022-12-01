import sys


class NodeColor:
    """
    This class represents the color of the tree. It can either be red or black
    """
    RED = 1
    BLACK = 2

    @staticmethod
    def get_color(color):
        if color == NodeColor.RED:
            return "R"
        else:
            return "B"


class TreeNode:
    """
        This class represents a single node in red black tree
    """
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
            return 'node found in the tree: value: ' + str(self.value) + ', color: ' + NodeColor.get_color(self.color) + '\n'


class RedBlackTree:
    def __init__(self):
        self.Tree_Node_NULL = TreeNode(-sys.maxsize - 1)
        self.Tree_Node_NULL.color = NodeColor.BLACK
        self.Tree_Node_NULL.left = None
        self.Tree_Node_NULL.right = None
        self.root = self.Tree_Node_NULL
        self.log_level = 1

    # ------ start: helper functions
    def log(self, log_string):
        if self.log_level > 0:
            print(log_string)

    def print_tree(self, current_node, level=1):
        """
            Print the tree rotated 90 degrees to the left. So we will have right nodes at the top and
            left nodes at the bottom.
        """
        if current_node != self.Tree_Node_NULL:
            self.print_tree(current_node.right, level + 1)
            print(' ' * 12 * level + '----> ' + str(current_node.value) + ', c:' + NodeColor.get_color(
                current_node.color) + ', l:' + str(level))
            self.print_tree(current_node.left, level + 1)
        else:
            if self.log_level > 1:
                print(' ' * 12 * level + '----> NULL Node')

    def min(self, current_node):
        while current_node.left != self.Tree_Node_NULL:
            current_node = current_node.left
        return current_node

    def maximum(self, current_node):
        while current_node.right != self.Tree_Node_NULL:
            current_node = current_node.right
        return current_node

    def left_rotate(self, current_node):
        """
            Here we perform left rotation around the nodes provided.
        """
        self.log('Left rotating - [' + str(current_node.value) + ']')
        c_right_node = current_node.right
        current_node.right = c_right_node.left
        if c_right_node.left != self.Tree_Node_NULL:
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

        self.print_tree(self.root)
        print('\n')

    def right_rotate(self, current_node):
        """
            Here we perform right rotation around the nodes provided.
        """
        self.log('Right rotating - [' + str(current_node.value) + ']')
        c_left_node = current_node.left
        current_node.left = c_left_node.right
        if c_left_node.right != self.Tree_Node_NULL:
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

        self.print_tree(self.root)
        print('\n')
    # ------ end: helper functions

    # ------ start: searching a node
    # Search the red black tree
    def _search_red_black_tree(self, search_node, node_value):
        if search_node == self.Tree_Node_NULL or node_value == search_node.value:
            return search_node

        if node_value < search_node.value:
            return self._search_red_black_tree(search_node.left, node_value)

        return self._search_red_black_tree(search_node.right, node_value)

    def search_red_black_tree(self, node_value):
        self.log('Searching for node - [' + str(node_value) + '] in the tree')
        return self._search_red_black_tree(self.root, node_value)
    # ------ end: searching a node

    # ------ start: deleting a node
    # Balancing the tree after deletion
    def balance_after_delete(self, c_node):
        """
            To balance the tree after deleting a node we check following conditions
            - If the node to be deleted is red color and leaf node, just deleted it.
            - If the node to be deleted is red color and has single black child, just deleted it.
            - If node to be deleted is black and it’s sibling is red then delete the node and perform left/right
            rotation on parent node.
            - If node to be deleted is black and it’s sibling is black then
                > If sibling has both black children perform recoloring by making sibling red and sibling’s parent
                  black. Continue rebalancing to the top.
                > If sibling has red children then perform required rotation
        """
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
        c_node.color = NodeColor.BLACK

    # this is the transplant function in the BST
    def replace_node(self, node_to_be_deleted, node_to_be_replaced_with):
        """
            Replace the node based on what side the current node is with respect to the parent.
            Set the current node's parent to the replacement node's parent.
        """
        if node_to_be_deleted.parent is None:
            self.root = node_to_be_replaced_with
        elif node_to_be_deleted == node_to_be_deleted.parent.left:
            node_to_be_deleted.parent.left = node_to_be_replaced_with
        else:
            node_to_be_deleted.parent.right = node_to_be_replaced_with

        node_to_be_replaced_with.parent = node_to_be_deleted.parent
        self.print_tree(self.root)

    # Node deletion
    def _delete_node(self, current_node, node_value):
        """
            Search for the node in the tree, if found delete it and find the replacement node.
            We only delete the leaf nodes so we perform replacement operations when deleting a node that has
            more than one children.
        """
        node_to_be_deleted = self.Tree_Node_NULL

        # search the node to be deleted
        while current_node != self.Tree_Node_NULL:
            if current_node.value == node_value:
                node_to_be_deleted = current_node

            if current_node.value <= node_value:
                current_node = current_node.right
            else:
                current_node = current_node.left

        if node_to_be_deleted == self.Tree_Node_NULL:
            print('Delete operation: Cannot find node [' + str(node_value) + '] in the tree')
            return

        t_node_to_be_deleted = node_to_be_deleted
        t_node_to_be_deleted_original_color = t_node_to_be_deleted.color

        if node_to_be_deleted.right == self.Tree_Node_NULL:
            replace_node = node_to_be_deleted.left
            print('Delete operation: replacing with left node of [' + str(node_to_be_deleted.value) + ']')
            self.replace_node(node_to_be_deleted, node_to_be_deleted.left)
        elif node_to_be_deleted.left == self.Tree_Node_NULL:
            replace_node = node_to_be_deleted.right
            print('Delete operation: replacing with right node of [' + str(node_to_be_deleted.value) + ']')
            self.replace_node(node_to_be_deleted, node_to_be_deleted.right)
        else:
            # find the successor to replace the node
            t_node_to_be_deleted = self.min(node_to_be_deleted.right)
            print('Delete operation: replacing node [' + str(node_to_be_deleted.value) + '] with successor node [' + str(t_node_to_be_deleted.value) + ']')
            t_node_to_be_deleted_original_color = t_node_to_be_deleted.color
            replace_node = t_node_to_be_deleted.right
            if t_node_to_be_deleted.parent == node_to_be_deleted:
                replace_node.parent = t_node_to_be_deleted
            else:
                self.replace_node(t_node_to_be_deleted, t_node_to_be_deleted.right)
                t_node_to_be_deleted.right = node_to_be_deleted.right
                t_node_to_be_deleted.right.parent = t_node_to_be_deleted

            self.replace_node(node_to_be_deleted, t_node_to_be_deleted)
            t_node_to_be_deleted.left = node_to_be_deleted.left
            t_node_to_be_deleted.left.parent = t_node_to_be_deleted
            t_node_to_be_deleted.color = node_to_be_deleted.color

        if t_node_to_be_deleted_original_color == NodeColor.BLACK:
            self.balance_after_delete(replace_node)

    def delete_node(self, node_value):
        self.log('Deleting node - [' + str(node_value) + ']')
        self._delete_node(self.root, node_value)
        print('Delete completed, final tree ')
        self.print_tree(self.root)
    # ------ end: deleting new node

    # ------ start: inserting new node
    # iteratively balance the tree after insertion
    def balance_tree_after_insert(self, current_node):
        """
            To balance a tree after inserting a new node we perform following steps
            - Recolor if parent’s sibling is red color
            - Rotation is done when parent’s sibling is black color
                > Rotation has four cases LL, LR, RR, RL
                > LR is performed by doing left rotation on parent and then right rotation on grandparent
                > RL is performed by doing right rotation on parent and then left rotation on grandparent
        """
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
        """
            Insert a node like BST and call re-balancing
        """
        self.log('Inserting node - [' + str(node_value) + ']')
        new_node = TreeNode(node_value)
        new_node.parent = None
        new_node.value = node_value
        new_node.left = self.Tree_Node_NULL
        new_node.right = self.Tree_Node_NULL
        new_node.color = NodeColor.RED

        new_node_parent = None
        current_node = self.root

        while current_node != self.Tree_Node_NULL:
            new_node_parent = current_node
            if new_node.value == current_node.value:
                print('The node with value [' + str(node_value) + '] already exists in the tree')
                return
            elif new_node.value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right

        new_node.parent = new_node_parent
        if new_node_parent is None:
            self.root = new_node
        elif new_node.value < new_node_parent.value:
            new_node_parent.left = new_node
        else:
            new_node_parent.right = new_node

        self.print_tree(self.root)
        print('\n\n')

        if new_node.parent is None:
            new_node.color = NodeColor.BLACK
            return

        if new_node.parent.parent is None:
            return

        self.balance_tree_after_insert(new_node)

    # ------ end: inserting new node
