
import ast
import networkx as nx


"""
    Generate a Control Flow Graph (CFG) from Python code using the `ast` module
"""

def code_to_cfg(tree):
    # Parse the code and generate an abstract syntax tree (AST)
    

    # Traverse the AST and build the control flow graph
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            # If statement
            cfg[node.lineno] = [node.body[0].lineno]
            if node.orelse:
                cfg[node.lineno].append(node.orelse[0].lineno) 
                code_to_cfg(node.orelse[0])
        elif isinstance(node, ast.While):
            # While loop
            cfg[node.lineno] = [node.test.lineno, node.body[0].lineno]
        elif isinstance(node, ast.For):
            # For loop
            cfg[node.lineno] = [node.iter.lineno, node.body[0].lineno]
        elif isinstance(node, ast.FunctionDef):
            # Function definition
            cfg[node.lineno] = [node.body[0].lineno]

    # Convert the dictionary to an array of directed edges
    edges = []
    for start, targets in cfg.items():
        for target in targets:
            edges.append((start, target))

    return edges


    
code = """def foo(n):
    if n == 0:
        x=3
        return 1
    elif n==1:
        return n * foo(n - 1)
    else:
        return 2
"""

tree = ast.parse(code)
cfg = {}
print(code_to_cfg(tree))

