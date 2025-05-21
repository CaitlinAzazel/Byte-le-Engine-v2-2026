import re

from game.config import ALLOWED_MODULES


def verify_code(filename: str) -> ([], bool, bool):
    """
    This file is used to verify a client's code. It helps to prevent certain attempts at purposefully interfering with the
    code and competition.
    """
    with open(filename, 'r') as f:
        contents = f.read()

    # Use regex to exclude comments from flagging a base_client.py file as invalid
    contents = re.sub(
        "#.*$|\"\"\"[\\S\\s]*?\"\"\"|'''[\\S\\s]*?'''|\"[^\"].*?[^\\\\]\"|'[^'].*?[^\\\\]'", "", contents
    ).splitlines()

    illegal_imports = list()
    uses_open = False
    uses_print = False

    for line in contents:
        line = re.split('[ ;]', line)
        for token in line:
            if '#' in token:
                break

            # Check for illegal keywords
            if 'from' == token:
                module = line[line.index('from') + 1]
                if module not in ALLOWED_MODULES:
                    illegal_imports.append(module)
                else:
                    break
            elif 'import' == token:
                module = line[line.index('import') + 1]
                if module not in ALLOWED_MODULES:
                    illegal_imports.append(module)
                else:
                    break
            uses_open = 'open(' in token

            uses_print = 'print(' in token

    return illegal_imports, uses_open, uses_print

def verify_num_clients(clients, set_clients, min_clients, max_clients):
    res = None
    # Verify correct number of clients
    if set_clients is not None and len(clients) != set_clients:
        res = ValueError("Number of clients is not the set value.\n"
                         "Number of clients: " + str(len(clients)) + "  |  Set number: " + str(set_clients))
    elif min_clients is not None and len(clients) < min_clients:
        res = ValueError("Number of clients is less than the minimum required.\n"
                         "Number of clients: " + str(len(clients)) + "  |  Minimum: " + str(min_clients))
    elif max_clients is not None and len(clients) > max_clients:
        res = ValueError("Number of clients exceeds the maximum allowed.\n"
                         "Number of clients: " + str(len(clients)) + "  |  Maximum: " + str(max_clients))

    return res
