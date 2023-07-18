import random
import Tree
import show_tree

operators = ["+", "-", "*", "/"]
operands = [str(i+1) for i in range(9)]
# length of random input that we created
first_exp = 10
# length of our first Gen
len_run = 1000
# how many crossover we do
len_crossover = int(len_run/2)
# choose  some part for creating next Gen
best_of_gens = int(len_run/10)

# make len_run random func for instance


def random_generation():
    operand = random.choice(operands)
    expression = []
    expression.append(operand)
    check_x = False
    for i in range(first_exp):
        if(expression.__contains__("x")):
            check_x = True
        operator = random.choice(operators)
        operand = random.choice(operands)
        expression.append(operator)
        expression.append(operand)
    if(check_x == False):
        while(True):
            random_replace = random.randint(0, len(expression)-1)
            if Tree.isOperator(expression[random_replace]) == False:
                expression[random_replace] = "x"
                break
    i = 0
    while i < len(expression):
        if expression[i] == "*" or expression[i] == "/":
            temp = expression[i-1]
            expression[i-1] = "(" + temp
            j = i+2
            while(j < len(expression)):
                if(expression[j] == "*" or expression[j] == "/"):
                    j = j+2
                else:
                    new_temp = expression[j-1]
                    expression[j-1] = new_temp + ")"
                    break
        i = i + 1
    # for i in range(len(expression)):
    final_exp = "".join(expression)
    while final_exp.count("(") != final_exp.count(")"):
        final_exp = final_exp + ")"
    return final_exp


# fill our first list out with random input


def make_funct(funct_list):
    for i in range(len_run):
        new_funct = random_generation()
        funct_list.append(new_funct)

# make tree


def make_tree(funct, tree):
    for i in range(len(funct)):
        postfix = Tree.infix_to_postfix(funct[i])
        r = Tree.constructTree(postfix)
        tree.append(r)


def nemune(tree):
    x = input("Enter the X: ")
    for i in range(len_run):
        Tree.Inorder(tree[i])
        print(Tree.evaluate(tree[i], float(x)))
        print("")

# find how our solution is


def fitness(tree, input_list, output_list):
    total_diff = 0
    for j in range(len(input_list)):
        dis_val = Tree.evaluate(tree, float(input_list[j]))
        total_diff += abs(dis_val - output_list[j])
    if total_diff == 0:
        return 99999
    else:
        return 1 / total_diff

# fill fitness_list with our info and return its sorted


def calc_fit(fitness_list, tree_list, input_list, output_list):
    fitness_list.clear()
    for i in range(len_run):
        fitness_list.append((tree_list[i], fitness(
            tree_list[i], input_list, output_list)))
    max_fit = sorted(
        fitness_list, key=lambda fitness_list: fitness_list[1], reverse=True)
    return max_fit


# find 2 nodes from different tree and swap their it and its child with each other
def crossover(treelist):
    tree1 = random.choice(treelist)
    tree2 = random.choice(treelist)
    Tree.select_change_node(tree1, tree2)

# change a node value


def mutation(select_tree):
    tree = Tree.mutation_tree_node(select_tree)
    return tree

# change 2 nodes value with swapping


def swap_mutation(select_tree):
    tree = Tree.swap_mutation_tree_node(select_tree)
    return tree


# in this part we choose an input give it to black box and get output ,then we check how similar our func is to black box


# input_list = [1, 2, 3, 4, 5 , 6, 7, 8, 9, 10] ;output_list = [2, 5, 8, 10, 12 , 18, 20, 27, 10, 11]
input_list = [1, 2, 3, 4, 5]
output_list = [2, 5, 8, 10, 12]
# input_list = [7,9,10,44,1, 2, 3, 4, 5] ;output_list = [10,12,30,20,2, 5, 8, 10, 12]
# input_list = [2, 3, 4, 8, 10, 12] ;output_list = [10 , 15 , 8, 10, 12 , 20]
# input_list = [8, 11, 14, 18, 3, 4, 5] ; output_list = [14 ,8,20,42,35 10, 12]
# input_list = [2, 4, 6, 8, 10, 12, 20, 27, 30, 45];output_list = [10, 20, 30, 40, 45, 60, 80, 99, 110, 150]

# getting first gen of function and store
funct_list = []
# make tree of func we created
tree_list = []
# return a tuple that  contains a tree and its fitness number(bigger , better)
fitness_list = []
# sorted fitness func
max_fit = []

# func that append input func to Funct_list
make_funct(funct_list)

# make tree of funct_lsit
make_tree(funct_list, tree_list)

# nemune(tree)
# for i in range(16):
#     fitness_list.append((tree_list[i], fitness(
#         tree_list[i], input_list, output_list)))

# return best of func we create
best_of_all = None
for h in range(10):
    # make fitness_list
    max_fit = calc_fit(fitness_list, tree_list, input_list, output_list)
    # assign value and check for finding the best function
    if h == 0:
        best_of_all = max_fit[:1]
    if best_of_all[0][1] < max_fit[0][1]:
        best_of_all = max_fit[:1]
    # end answer
    show_tree.display(max_fit[0][0])
    print(f"gen {h} best is {max_fit[0]} ")

    best_solutions = max_fit[:best_of_gens]
    for i in range(len_crossover):
        # tree_list
        crossover([i[0] for i in best_solutions])
    # for i in range(len_crossover):
    #     crossover(tree_list)

    # make a list and fill the Tree_list out with it
    New_Gen = []
    for _ in range(int(len_run/best_of_gens)):
        for i in range(best_of_gens):
            new_tree = mutation(best_solutions[i][0])
            New_Gen.append(new_tree)
    # New_Gen = []
    # for _ in range(int(len_run/best_of_gens)):
    #     for i in range(best_of_gens):
    #         new_tree = swap_mutation(best_solutions[i][0])
    #         New_Gen.append(new_tree)

    tree_list = New_Gen

# show the best of all
print("best answer is :")
print(best_of_all)
show_tree.display(best_of_all[0][0])
# Tree.infix_expTree(best_of_all[0][0])
