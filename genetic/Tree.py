from collections import deque
import random
import show_tree


operators = ["+", "-", "*", "/"]
operands = [i+1 for i in range(9)]


def isOperator(c):
    if (c == '+' or
       c == '-' or
       c == '*' or
       c == '/' or
       c == '^'):
        return True
    else:
        return False

# class for making expression tree


class Node:
    def __init__(self, root_value):
        self.left = None
        self.right = None
        self.val = root_value

# eval how much is value of our expression tree


def evaluate(node, Sepcial_value) -> float:
    if isOperator(node.val) == False:
        if(node.val == "x"):
            return Sepcial_value
        else:
            node.val = float(node.val)
            val1 = float(node.val)
            return val1
    # recurssively call func to eval all the nodes
    left_value = evaluate(node.left, Sepcial_value)
    right_value = evaluate(node.right, Sepcial_value)
    # addition
    if node.val == "+":
        return left_value + right_value
    # subtraction
    elif node.val == "-":
        return left_value - right_value
    # division
    elif node.val == "/":
        # if some 0 happens in Denominator ,put it 1
        if (right_value == 0):
            right_value = 1
        return left_value / right_value
    # multiplication
    elif node.val == "*":
        return left_value * right_value
    # power
    else:
        return left_value ** right_value

# travers the expression tree Inorder


def Inorder(root):
    if root:
        Inorder(root.left)
        print(root.val, end=" ")
        Inorder(root.right)

# infix to postfix for making expression tree


def infix_to_postfix(infix_input: list) -> list:

    # precedence order and associativity helps to determine which
    precedence_order = {'+': 0, '-': 0, '*': 1, '/': 1, '^': 2}
    associativity = {'+': "LR", '-': "LR", '*': "LR", '/': "LR", '^': "RL"}
    # clean the infix expression
    clean_infix = infix_input

    i = 0
    postfix = []
    operators = "+-/*^"
    stack = deque()
    while i < len(clean_infix):

        char = clean_infix[i]
        # check if char is operator
        if char in operators:
            # check if the stack is empty or the top element is '('
            if len(stack) == 0 or stack[0] == '(':
                # just push the operator into stack
                stack.appendleft(char)
                i += 1
            # otherwise compare the curoot char with top of the element
            else:
                # peek the top element
                top_element = stack[0]
                # check for precedence
                # if they have equal precedence
                if precedence_order[char] == precedence_order[top_element]:
                    # check for associativity
                    if associativity[char] == "LR":
                        # pop the top of the stack and add to the postfix
                        popped_element = stack.popleft()
                        postfix.append(popped_element)
                    # if associativity of char is Right to left
                    elif associativity[char] == "RL":
                        # push the new operator to the stack
                        stack.appendleft(char)
                        i += 1
                elif precedence_order[char] > precedence_order[top_element]:
                    # push the char into stack
                    stack.appendleft(char)
                    i += 1
                elif precedence_order[char] < precedence_order[top_element]:
                    # pop the top element
                    popped_element = stack.popleft()
                    postfix.append(popped_element)
        elif char == '(':
            # add it to the stack
            stack.appendleft(char)
            i += 1
        elif char == ')':
            top_element = stack[0]
            while top_element != '(':
                popped_element = stack.popleft()
                postfix.append(popped_element)
                # update the top element
                top_element = stack[0]
            # now we pop opening parenthases and discard it
            stack.popleft()
            i += 1
        # char is operand
        else:
            postfix.append(char)
            i += 1

    # empty the stack
    if len(stack) > 0:
        for i in range(len(stack)):
            postfix.append(stack.popleft())

    return postfix


# make expression tree form postfix
def constructTree(postfix):
    stack = []
    for char in postfix:
        mytree = Node(char)
        if isOperator(char):
            t1 = stack.pop()
            t2 = stack.pop()
            mytree.right = t1
            mytree.left = t2
        stack.append(mytree)
    mytree = stack.pop()
    return mytree

# find all nodes of expression tree bt travers


def All_Nodes(root, mylist):
    if root:
        All_Nodes(root.left, mylist)
        mylist.append([root.val, root])
        All_Nodes(root.right, mylist)

# find parent if we have it and return it


def check_parent(root, goal):
    if root:
        if (root.left and root.left == goal) or (root.right and root.right == goal):
            return root or check_parent(root.left, goal) or check_parent(root.right, goal)
        else:
            return check_parent(root.left, goal) or check_parent(root.right, goal)


# for crossvoer
def select_change_node(root1, root2):
    #print(root1, root2)
    list_nodes1 = []
    list_nodes2 = []
    All_Nodes(root1, list_nodes1)
    All_Nodes(root2, list_nodes2)
    # choose random node from a tree
    selected_node1 = random.choice(list_nodes1)
    selected_node2 = random.choice(list_nodes2)

    # check situation if 2 tree's random chose is  operators , operands or they're not root because root doesn't have parent
    while((not isOperator(selected_node1[0]) and isOperator(selected_node2[0])) or
          (isOperator(selected_node1[0]) and (not isOperator(selected_node2[0]))) or
            selected_node1[1] == root1 or selected_node2[1] == root2):
        selected_node1 = random.choice(list_nodes1)
        selected_node2 = random.choice(list_nodes2)
    # print(selected_node1, selected_node2)

    # find nodes parent for change
    parent1 = check_parent(root1, selected_node1[1])
    parent2 = check_parent(root2, selected_node2[1])

    # sawp
    if(parent1.right == selected_node1[1] and parent2.right == selected_node2[1]):
        # print(1)
        parent1.right, parent2.right = parent2.right, parent1.right
    if(parent1.left == selected_node1[1] and parent2.right == selected_node2[1]):
        # print(2)
        parent1.left, parent2.right = parent2.right, parent1.left
    if(parent1.right == selected_node1[1] and parent2.left == selected_node2[1]):
        # print(3)
        parent1.right, parent2.left = parent2.left, parent1.right
    if(parent1.left == selected_node1[1] and parent2.left == selected_node2[1]):
        # print(4)
        parent1.left, parent2.left = parent2.left, parent1.left
    # print(parent1.val)


# for mutation
def mutation_tree_node(root):
    list_nodes = []
    parent1 = Node(-1)
    All_Nodes(root, list_nodes)
    node_for_change = random.choice(list_nodes)

    # print(node_for_change)
    if node_for_change[1] == root:
        root.val = random.choice(operators)
    else:
        parent1 = check_parent(root, node_for_change[1])

        if(parent1.right == node_for_change[1]):

            if isOperator(node_for_change[0]):
                parent1.right.val = random.choice(operators)

            else:
                parent1.right.val = random.choice(operands)
        elif(parent1.left == node_for_change[1]):

            if isOperator(node_for_change[0]):
                parent1.left.val = random.choice(operators)

            else:
                parent1.left.val = random.choice(operands)
    return root


# for swap mutation
def swap_mutation_tree_node(root):

    list_nodes = []
    parent1 = Node(-1)
    parent2 = Node(-1)
    All_Nodes(root, list_nodes)
    node_for_swap1 = random.choice(list_nodes)
    node_for_swap2 = random.choice(list_nodes)

    while((not isOperator(node_for_swap1[0]) and isOperator(node_for_swap2[0])) or
            (isOperator(node_for_swap1[0]) and (not isOperator(node_for_swap2[0]))) or
            node_for_swap1 == node_for_swap2):
        node_for_swap1 = random.choice(list_nodes)
        node_for_swap2 = random.choice(list_nodes)

    #print(node_for_swap1, node_for_swap2)
    if node_for_swap1[1] == root:
        parent1.right = root
        parent2 = check_parent(root, node_for_swap2[1])
    elif node_for_swap2[1] == root:
        parent1 = check_parent(root, node_for_swap1[1])
        parent2.right = root
    else:
        parent1 = check_parent(root, node_for_swap1[1])
        parent2 = check_parent(root, node_for_swap2[1])

    # change value
    if(parent1.right == node_for_swap1[1] and parent2.right == node_for_swap2[1]):
        # print(1)
        parent1.right.val, parent2.right.val = parent2.right.val, parent1.right.val
    if(parent1.left == node_for_swap1[1] and parent2.right == node_for_swap2[1]):
        # print(2)
        parent1.left.val, parent2.right.val = parent2.right.val, parent1.left.val
    if(parent1.right == node_for_swap1[1] and parent2.left == node_for_swap2[1]):
        # print(3)
        parent1.right.val, parent2.left.val = parent2.left.val, parent1.right.val
    if(parent1.left == node_for_swap1[1] and parent2.left == node_for_swap2[1]):
        # print(4)
        parent1.left.val, parent2.left.val = parent2.left.val, parent1.left.val
    return root

# change expression tree to  infix


def infix_expTree(root):
    if root != None:
        if root.left != None and root.right != None:
            print("(", end='')
        infix_expTree(root.left)
        print(root.val, end='')
        infix_expTree(root.right)
        if root.left != None and root.right != None:
            print(")", end='')

# an instance of mutation and crossover


# a = "((x+5)/3)-(3+8)"
# b = "((x+5)-3)-((3-8)+((x-5)*3))"

# postfix1 = infix_to_postfix(a)
# postfix2 = infix_to_postfix(b)
# tree1 = constructTree(postfix1)
# tree2 = constructTree(postfix2)
# show_tree.display(tree1)
# for i in range(10):
#     print("")
# show_tree.display(tree2)
# # select_change_node(tree1, tree2)
# treelist = []
# treelist.append(tree1)
# treelist.append(tree2)
# for i in range(len(treelist)):
#     # mutation_tree_node(treelist[i])
#     swap_mutation_tree_node(treelist[i])

# show_tree.display(treelist[0])
# for i in range(10):
#     print("")
# show_tree.display(treelist[1])
