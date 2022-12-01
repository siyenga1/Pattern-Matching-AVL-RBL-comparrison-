import sys

from avl.avl import AVLTree
from boyerMoore.boyerMooreSearch import BoyerMooreSearch
from kmp.kmp import KMP
from redBlackTree.redBlackTree import RedBlackTree


def main():
    while True:
        print("\nLIST OF ALGORITHMS:- ")
        print("1. Knuth Morris Pratt Algorithm")
        print("2. Red Black Trees Algorithm")
        print("3. Adelson-Velskii and Landis(AVL) Trees Algorithm")
        print("4. Boyer Moore Algorithm")
        print("5. Exit")
        try:
            choice = int(input("Enter the Choice:"))
        except:
            print("Incorrect Format of the choice")
            sys.exit(1)

        if choice == 1:
            kmp = KMP()
            kmp.myInput()
        elif choice == 2:
            rbt = RedBlackTree()
            while True:
                print("\n********************* WELCOME TO RED BLACK Tree *******************")
                print("\nOperations to Perform on Tree:- ")
                print("1. Insert")
                print("2. Delete")
                print("3. Search")
                print("4. Pretty Print Tree")
                print("5. Go Back to Previous Menu")
                try:
                    rbtchoice = int(input("Enter the Choice:"))
                except:
                    print("Incorrect Format of the choice")
                    sys.exit(1)
                if rbtchoice == 1:
                    try:
                        key = int(input("Enter the Key to insert:"))
                    except:
                        print("Incorrect Format of the key.")
                        sys.exit(1)
                    rbt.insert(key)
                elif rbtchoice == 2:
                    try:
                        key = int(input("Enter the Key to remove:"))
                    except:
                        print("Incorrect Format of the key")
                        sys.exit(1)
                    rbt.delete_node(key)
                elif rbtchoice==3:
                    try:
                        key = int(input("Enter the Key to search:"))
                    except:
                        print("Incorrect Format of the key.")
                        sys.exit(1)
                    n = rbt.search_tree(key)
                    if n:
                        print("Node found: ", str(n))
                    else:
                        print("Node with key not found")
                elif rbtchoice==4:
                    rbt.print_tree(rbt.root)
                elif rbtchoice==5:
                    print("Going back to Main Menu")
                    break
                else:
                    print("Please enter the correct choice")

        elif choice == 3:
            avl = AVLTree()
            while True:
                print("\n********************* WELCOME TO AVL Tree *******************")
                print("\nOperations to Perform on Tree:- ")
                print("1. Insert")
                print("2. Delete")
                print("3. Search")
                print("4. Pretty Print Tree")
                print("5. Go Back to Previous Menu")
                try:
                    avlchoice = int(input("Enter the Choice:"))
                except:
                    print("Incorrect Format of the choice")
                    sys.exit(1)
                if avlchoice==1:
                    try:
                        key = int(input("Enter the Key to insert:"))
                    except:
                        print("Incorrect Format of the key")
                        sys.exit(1)
                    avl.insert(key)
                elif avlchoice==2:
                    try:
                        key = int(input("Enter the Key to remove:"))
                    except:
                        print("Incorrect Format of the key")
                        sys.exit(1)
                    avl.delete(key)
                elif avlchoice==3:
                    try:
                        key = int(input("Enter the Key to search:"))
                    except:
                        print("Incorrect Format of the key")
                        sys.exit(1)
                    _, n = avl.search(key)
                    if n:
                        print("Node found: ", n)
                    else:
                        print("Node with key not found")
                elif avlchoice==4:
                    avl.printTree()
                # elif avlchoice==5:
                #     avl.printInOrder()
                # elif avlchoice==6:
                #     avl.printPreOrder()
                # elif avlchoice==7:
                #     avl.printPostOrder()
                elif avlchoice==5:
                    print("Going back to Main Menu")
                    break
                else:
                    print("Please enter the correct choice")


        elif choice == 4:
            print("*********************WELCOME TO BOYER MOORE SEARCH ALGORITHM*******************")
            boyerMoore = BoyerMooreSearch()
            string = input("Please enter the first input string ")
            pattern = input("Please enter the pattern to be matched ")
            if len(string)==0 or len(pattern)==0:
                print("Empty String or Empty Pattern")
            else:
                boyerMoore.search(string, pattern)

        elif choice == 5:
            print("EXITING NOW...")
            sys.exit(1)
        else:
            print("Please enter the correct choice")

        print("")
        print("Please enter the next algorithm you want to try or exit")
    end


if __name__ == "__main__":
    main()
