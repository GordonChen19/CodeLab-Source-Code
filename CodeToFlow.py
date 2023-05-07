import ast
import networkx as nx
import matplotlib.pyplot as plt


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
            cfg.add_edge(id(node.test), id(node.body[0]))
            if node.orelse:
                cfg.add_edge(id(node.test), id(node.orelse[0]))
        elif isinstance(node, ast.While):
            # While loop
            cfg.add_edge(id(node.test), id(node.body[0]))
            cfg.add_edge(id(node.test), id(node))
            cfg.add_edge(id(node), id(node.test))
        elif isinstance(node, ast.For):
            # For loop
            cfg.add_edge(id(node.iter), id(node.target))
            cfg.add_edge(id(node.iter), id(node.body[0]))
            cfg.add_edge(id(node.body[-1]), id(node.iter))
        elif isinstance(node, ast.Try):
            # Try/except block
            for handler in node.handlers:
                cfg.add_edge(id(handler), id(handler.body[0]))
            if node.orelse:
                cfg.add_edge(id(node), id(node.orelse[0]))
        elif isinstance(node, ast.With):
            # With statement
            cfg.add_edge(id(node.context_expr), id(node.body[0]))
        elif isinstance(node, ast.FunctionDef):
            # Function definition
            cfg.add_edge(id(node.args), id(node.body[0]))
            for n in node.body:
                if isinstance(n, ast.Return):
                    cfg.add_edge(id(n), id(node))
        elif isinstance(node, ast.Return):
            # Return statement
            cfg.add_edge(id(node), id(node.value))
        elif isinstance(node, ast.Break):
            # Break statement
            cfg.add_node(id(node))
        elif isinstance(node, ast.Continue):
            # Continue statement
            cfg.add_node(id(node))
        elif isinstance(node, ast.Expr):
            # Expression statement
            cfg.add_edge(id(node), id(node.value))
        elif isinstance(node, ast.Assign):
            # Assignment statement
            cfg.add_edge(id(node.value), id(node.targets[0]))

    # Draw the CFG using matplotlib
    pos = nx.drawing.nx_agraph.graphviz_layout(cfg, prog='dot')
    nx.draw_networkx_nodes(cfg, pos)
    nx.draw_networkx_edges(cfg, pos)
    nx.draw_networkx_labels(cfg, pos)
    plt.show()
    
    
code = """
def foo(n):
    if n == 0:
        return 1
    else:
        return n * foo(n - 1)
"""

code_to_cfg(code)
