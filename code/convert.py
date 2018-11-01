def dict_from_node(node):
    return {node.tag : list(map(dict_from_node, node)) or node.text}

def dict_from_dicts(list_of_dicts):
    return { key : value for _dict in list_of_dicts for key , value in _dict.items() }

def list_from_dicts(list_of_dicts):
    return [ dict_from_dicts( value ) for _dict in list_of_dicts for value in _dict.values( ) ]
