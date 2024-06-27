import re

# Sample collection of documents
documents = [
    {"doc_id": 1, "content": "python is a programming language"},
    {"doc_id": 2, "content": "python is popular for data analysis"},
    {"doc_id": 3, "content": "java is also a programming language"},
    {"doc_id": 4, "content": "java is used in enterprise applications"},
    {"doc_id": 5, "content": "python and java are both languages"},
]

def tokenize_query(query):
    """Tokenizes the query into terms and operators."""
    return re.findall(r'\w+|AND|OR|NOT|\(|\)', query.upper())

def retrieve_documents(query):
    """Retrieves documents based on the Extended Boolean Model query."""
    tokens = tokenize_query(query)
    result_docs = set(range(1, len(documents) + 1))  # Start with all documents

    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        if token == '(':
            j = i + 1
            while j < len(tokens):
                if tokens[j] == ')':
                    subquery_tokens = tokens[i+1:j]
                    subquery_result = retrieve_documents(" ".join(subquery_tokens))
                    result_docs.intersection_update(subquery_result)
                    i = j  # Move index past the closing parenthesis
                    break
                j += 1
        elif token == 'AND':
            j = i + 1
            while j < len(tokens):
                if tokens[j] in ('OR', ')'):
                    subquery_tokens = tokens[i+1:j]
                    subquery_result = retrieve_documents(" ".join(subquery_tokens))
                    result_docs.intersection_update(subquery_result)
                    i = j - 1  # Move index back to handle next token
                    break
                j += 1
        elif token == 'OR':
            j = i + 1
            while j < len(tokens):
                if tokens[j] in ('AND', ')'):
                    subquery_tokens = tokens[i+1:j]
                    subquery_result = retrieve_documents(" ".join(subquery_tokens))
                    result_docs.update(subquery_result)
                    i = j - 1  # Move index back to handle next token
                    break
                j += 1
        elif token == 'NOT':
            j = i + 1
            while j < len(tokens):
                if tokens[j] in ('AND', 'OR', ')'):
                    subquery_tokens = tokens[i+1:j]
                    subquery_result = retrieve_documents(" ".join(subquery_tokens))
                    result_docs.difference_update(subquery_result)
                    i = j - 1  # Move index back to handle next token
                    break
                j += 1
        else:
            # Token is a term
            if token in ('AND', 'OR', 'NOT'):
                continue
            term_docs = {doc["doc_id"] for doc in documents if token in doc["content"].lower()}
            result_docs.intersection_update(term_docs)

        i += 1
    
    return result_docs

# Example queries
query1 = "python AND language"
query2 = "python OR java"
query3 = "python AND NOT language"
query4 = "(python AND language) OR (java AND NOT applications)"

# Test queries
print(f"Query: {query1}")
print(f"Result: {[doc['doc_id'] for doc in documents if doc['doc_id'] in retrieve_documents(query1)]}")
print()

print(f"Query: {query2}")
print(f"Result: {[doc['doc_id'] for doc in documents if doc['doc_id'] in retrieve_documents(query2)]}")
print()

print(f"Query: {query3}")
print(f"Result: {[doc['doc_id'] for doc in documents if doc['doc_id'] in retrieve_documents(query3)]}")
print()

print(f"Query: {query4}")
print(f"Result: {[doc['doc_id'] for doc in documents if doc['doc_id'] in retrieve_documents(query4)]}")
