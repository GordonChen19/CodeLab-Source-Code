
import ast
import networkx as nx
import matplotlib.pyplot as plt


def code_to_cfg(code):
    """
    Generate a Control Flow Graph (CFG) from Python code using the `ast` module
    """
    # Parse the code into an AST
    tree = ast.parse(code)

    # Create a DiGraph to represent the CFG
    cfg = nx.DiGraph()

    # Walk the AST and add edges to the CFG
    for node in ast.walk(tree):
        if isinstance(node, ast.If):
            # If statement
            cfg.add_edge(node.test.lineno, node.body[0].lineno)
            if node.orelse:
                cfg.add_edge(node.test.lineno, node.orelse[0].lineno)
        elif isinstance(node, ast.While):
            # While loop
            cfg.add_edge(node.test.lineno, node.body[0].lineno)
            cfg.add_edge(node.test.lineno, node.lineno)
            cfg.add_edge(node.lineno, node.test.lineno)
        elif isinstance(node, ast.For):
            # For loop
            cfg.add_edge(node.iter.lineno, node.target.lineno)
            cfg.add_edge(node.iter.lineno, node.body[0].lineno)
            cfg.add_edge(node.body[-1].lineno, node.iter.lineno)
        elif isinstance(node, ast.Try):
            # Try/except block
            for handler in node.handlers:
                cfg.add_edge(handler.lineno, handler.body[0].lineno)
            if node.orelse:
                cfg.add_edge(node.lineno, node.orelse[0].lineno)
        elif isinstance(node, ast.With):
            # With statement
            cfg.add_edge(node.context_expr.lineno, node.body[0].lineno)
        elif isinstance(node, ast.FunctionDef):
            # Function definition
            print(f'function definition {node.lineno}')
            cfg.add_edge(node.lineno, node.body[0].lineno)
            for n in node.body:
                if isinstance(n, ast.Return):
                    cfg.add_edge(n.lineno, node.lineno)
        # elif isinstance(node, ast.Return):
        #     # Return statement
        #     if node.value:
        #         cfg.add_edge(node.lineno, node.value.lineno)
        #     else:
        #         cfg.add_edge(node.lineno, node.lineno)
        elif isinstance(node, ast.Break):
            # Break statement
            cfg.add_node(node.lineno)
        elif isinstance(node, ast.Continue):
            # Continue statement
            cfg.add_node(node.lineno)
        elif isinstance(node, ast.Expr):
            # Expression statement
            cfg.add_edge(node.lineno, node.value.lineno)
        elif isinstance(node, ast.Assign):
            # Assignment statement
            cfg.add_edge(node.value.lineno, node.targets[0].lineno)
            
    print(cfg.edges())


    
code = """
def foo(n):
    if n == 0:
        return 1
    else:
        return n * foo(n - 1)
"""

code_to_cfg(code)
