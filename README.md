# Information-Retrieval-Project
Studying Search Engines


# Collage Project
Process the documents (doc)...
[ ] Boolean model
[ ] Extended Boolean model
[ ] Vector model


# Abstracted Concepts:
## Read text from documents

## Boolean Model (Exact Match Model)
- An advantage of the Boolean model is that it gives (expert) users a sense of control over the system. It is immediately clear why a document has been retrieved, given a query.
- For untrained users, the model has a number of disadvantages. Its main disadvantade is that it does not provide a ranking of retrieved documents. The model is either ertrieves a document or not, which might lead to the system making rather frustrating decisions.

## Extended Boolean Model

## Vector Space Model
Hans Peter Luhn was the first to suggest a statistical model approach to searching information (Luhn 1957). He suggested that in order to search a document collection, the user should first prepare a document that is similar to the documents needed. The degree of similarity between the representation of the prepared document and the representation of the documents in the collection is used to rank the search results.

If the document's index representation is a vector `d` which each component is associated with an index term; and if a similar vector `q` of which the components are associated with the same terms, then a straightforward similarity measure is the vectors inner product

```
score(d,q) = d . q
```

[Continue](file:///C:/pyvm-SIR601/01_Books/9780470027622.excerpt.pdf)


## Probabilistic indexing model

## 2-Poisson model

## Bayesian network models

## Google's PageRank model

# Applied Concepts
## Query Processing
### Boolean Query processing
[Read more](https://medium.com/analytics-vidhya/boolean-retrieval-model-using-inverted-index-and-positional-index-2a9782bcec99)

Boolean queries are of type that contains Boolean Operators (AND, OR and NOT). Simple Boolean queries examples:

X AND Y: represents doc that contains both X and Y

X OR Y: represents doc that contains either X or Y

NOT X: represents the doc that do not contain X

Conjunctive Boolean queries examples:

(X AND Y) OR (Y AND Z) : represent doc that contain either both X and Y or Y and Z

(X AND Y) OR NOT Z : represent doc that contain either both X and Y or doc that do not contain Z.

Firstly the user query is converted to postfix expression in order to entertain both simple and conjunctive queries.

```
def postfix(infix_tokens):
    #precendence initialization
    precedence = {}
    precedence['NOT'] = 3
    precedence['AND'] = 2
    precedence['OR'] = 1
    precedence['('] = 0
    precedence[')'] = 0
    output = []
    operator_stack = []
 
    #creating postfix expression
    for token in infix_tokens:
    if (token == '('):
    operator_stack.append(token)

elif (token == ‘)’):
 operator = operator_stack.pop()
 while operator != ‘(‘:
 output.append(operator)
 operator = operator_stack.pop()
 
 elif (token in precedence):
 if (operator_stack):
 current_operator = operator_stack[-1]
 while (operator_stack and precedence[current_operator] > precedence[token]):
 output.append(operator_stack.pop())
 if (operator_stack):
 current_operator = operator_stack[-1]
operator_stack.append(token)
else:
 output.append(token.lower())
 
 #while staack is not empty appending
 while (operator_stack):
 output.append(operator_stack.pop())
 return output
```

The output is the sent to the process_query function to evaluate postfix expression.

```
def process_query(q,dictionary_inverted):
q = q.replace(‘(‘, ‘( ‘)
 q = q.replace(‘)’, ‘ )’)
 q = q.split(‘ ‘)
 query = []
for i in q:
 query.append(ps.stem(i))
 for i in range(0,len(query)):
 if ( query[i]== ‘and’ or query[i]== ‘or’ or query[i]== ‘not’):
 query[i] = query[i].upper()
 results_stack = []
 postfix_queue = postfix(query)
#evaluating postfix query expression
 for i in postfix_queue:
 if ( i!= ‘AND’ and i!= ‘OR’ and i!= ‘NOT’):
 i = i.replace(‘(‘, ‘ ‘)
 i = i.replace(‘)’, ‘ ‘)
 i = i.lower()
 i = dictionary_inverted.get(i)
 results_stack.append(i)
 elif (i==’AND’):
 a = results_stack.pop()
 b = results_stack.pop()
 results_stack.append(AND_op(a,b))
 elif (i==’OR’):
 a = results_stack.pop()
 b = results_stack.pop()
 results_stack.append(OR_op(a,b))
 elif (i == ‘NOT’):
 a = results_stack.pop()
 print(a)
 results_stack.append(NOT_op(a))
 
 return results_stack.pop()
```

AND, OR and NOT operation functions are as follows:



# Progress:
- [ ] Read the text from the documents

    - [X] (05/22/2024) [docx2text](https://pypi.python.org/pypi/docx2txt):

```
    import docx2txt
    my_text = docx2txt.process("file_path.docx")
    print(my_text)
```

- [ ] Boolean Model
    - [] Query Preocessing