import re

'''
def convert_to_sql_query(search_query):
    """
    Converts an advanced search query with AND, OR, and NOT operations into an SQL SQLite3 statement.
    By default, words are combined with AND operations.

    :param search_query: A string representing the advanced search query.
    :return: A tuple containing the SQL query and parameters.
    """
    # Split the search query into tokens by handling quoted phrases and AND/OR/NOT operators
    tokens = re.findall(r'"[^"]+"|\S+', search_query)
    
    sql_clauses = []
    query_params = []
    last_operator = None
    
    for token in tokens:
        if token in ('AND', 'OR', 'NOT'):
            last_operator = token.upper()
        else:
            if token.startswith('"') and token.endswith('"'):
                # Handle whole phrases
                token = token[1:-1]  # Remove surrounding quotes
                clause = "content LIKE ?"
                param = f'%{token}%'
            else:
                # Handle individual words
                clause = "content LIKE ?"
                param = f'%{token}%'
            
            if last_operator == 'NOT':
                clause = clause.replace('LIKE', 'NOT LIKE')
                last_operator = None  # Reset last_operator after use
            elif last_operator:
                sql_clauses.append(last_operator)
                last_operator = None  # Reset last_operator after use
            elif sql_clauses:
                sql_clauses.append('AND')  # Default operator is AND
            
            sql_clauses.append(clause)
            query_params.append(param)
    
    sql_query = "SELECT * FROM corpus WHERE " + " ".join(sql_clauses)
    return sql_query, query_params
'''
def parse_tokens(tokens):
    """
    Parse tokens into SQL clauses, supporting AND, OR, NOT, and brackets.
    """
    sql_clauses = []
    query_params = []
    stack = [[]]

    for token in tokens:
        if token.upper() in ('AND', 'OR'):
            stack[-1].append(token.upper())
        elif token.upper() == 'NOT':
            stack[-1].append('NOT')
        elif token == '(':
            stack.append([])
        elif token == ')':
            if len(stack) > 1:
                clause = stack.pop()
                if len(clause) == 1:
                    stack[-1].append(clause[0])
                else:
                    stack[-1].append(f"({' '.join(clause)})")
            else:
                raise ValueError("Unmatched closing parenthesis")
        else:
            if token.startswith('"') and token.endswith('"'):
                # Handle whole phrases
                token = token[1:-1]  # Remove surrounding quotes
                clause = "content LIKE ?"
                param = f'%{token}%'
            else:
                # Handle individual words
                clause = "content LIKE ?"
                param = f'%{token}%'

            if stack[-1] and stack[-1][-1] == 'NOT':
                clause = clause.replace('LIKE', 'NOT LIKE')
                stack[-1][-1] = clause
            else:
                stack[-1].append(clause)
            query_params.append(param)
    
    while len(stack) > 1:
        clause = stack.pop()
        stack[-1].append(f"({' '.join(clause)})")

    return ' '.join(stack[0]), query_params

def convert_to_sql_query(search_query):
    """
    Converts an advanced search query with AND, OR, NOT, and brackets into an SQL SQLite3 statement.
    By default, words are combined with AND operations.

    :param search_query: A string representing the advanced search query.
    :return: A tuple containing the SQL query and parameters.
    """
    # Split the search query into tokens by handling quoted phrases and AND/OR/NOT operators
    tokens = re.findall(r'"[^"]+"|\(|\)|\S+', search_query)
    sql_query, query_params = parse_tokens(tokens)
    sql_query = "SELECT * FROM corpus WHERE " + sql_query

    return sql_query, query_params

print(convert_to_sql_query("car AND (and AND dogs) OR \"super cars\" AND NOT here"))