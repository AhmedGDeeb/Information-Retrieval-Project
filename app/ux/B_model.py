# -- 
'''
Advanced search options
Find what you're looking for in less time. Use the following symbols to quickly modify your search term or search function:

Symbol

Function

+

Finds webpages that contain all the terms that are preceded by the + symbol. Also allows you to include terms that are usually ignored.

" "

Finds the exact words in a phrase.

()

Finds or excludes webpages that contain a group of words.

AND or &

Finds webpages that contain all the terms or phrases.

NOT or –

Excludes webpages that contain a term or phrase.

OR or |

Finds webpages that contain either of the terms or phrases.
'''

import re

class QueryProcesser():
    def process_query(self, *args):
        query_result = True
        """
        returns a tuple of:
        - list of docs (or empty list if not matches)

        throws a `ValueError` if the `query` is not valid. 
        """
        try:
            # TODO
            pass
        except ValueError as e:
            raise ValueError("Wrong Query!!")
        return query_result


class IRModel:
    def search(self, query, *args):
        docs = []
        return docs, 

class BooleanQueryProcessor(QueryProcesser):
    def process_query(self, query: str, doc_var_name = "doc"):
        """
        - remove extra spaces
        - remove ponctuaton
        - generate boolean experssion
        @ Params
        - `doc_var_name`: has .contains() function that returns True or False
        """
        query = query.strip()
        query = query.replace("(", " ( ")
        query = query.replace(")", " ) ")
        # TODO
        # remove additioanl white spaces
        query = query.split(" ")
        keywords = {
            "AND": "and", 
            "OR": "or", 
            "NOT": "not"
        }

        for q in range(len(query)):
            if query[q] == "(" or query[q] == ")":
                continue
            if query[q] in keywords.keys():
                query[q] = keywords[query[q]]
                continue
            query[q] = doc_var_name+".find('" + query[q] + "') != -1"

        return " ".join(query)


class BooleanModel(IRModel):
    def similarity(self, query, doc):
        pass

    def search(self, query, ):
        pass

class ExtendedBooleanModel(IRModel):
    pass

class VectorModel(IRModel):
    pass


# Code without tests is broken by design
import unittest
from test import support
class BooleanQueryProcessorTester(unittest.TestCase):
    def testAND(self):
        bm_qprocessor = BooleanQueryProcessor()
        AND_query = "infromation AND retreival"
        res = bm_qprocessor.process_query(AND_query)
        assert res == """doc.find('infromation') != -1 and doc.find('retreival') != -1"""
    
    def testOR(self):
        bm_qprocessor = BooleanQueryProcessor()
        AND_query = "infromation OR retreival"
        res = bm_qprocessor.process_query(AND_query)
        assert res == """doc.find('infromation') != -1 or doc.find('retreival') != -1"""
    
    def testANDNOT(self):
        bm_qprocessor = BooleanQueryProcessor()
        AND_query = "infromation AND NOT retreival"
        res = bm_qprocessor.process_query(AND_query)
        assert res == """doc.find('infromation') != -1 and not doc.find('retreival') != -1"""

    def testANDOR(self):
        bm_qprocessor = BooleanQueryProcessor()
        AND_query = "infromation OR NOT retreival"
        res = bm_qprocessor.process_query(AND_query)
        assert res == """doc.find('infromation') != -1 or not doc.find('retreival') != -1"""        

if __name__ == "__main__":
    unittest.main().runTests()