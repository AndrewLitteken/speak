from nltk.grammar import DependencyGrammar
from nltk.corpus import wordnet, stopwords
from nltk.parse import (
    DependencyGraph,
    ProjectiveDependencyParser,
    NonprojectiveDependencyParser
)
import nltk
from replacewords import replace
import sys
import spacy
import cgi
from flask import Flask
from flask import request
from flask import json
from Statement import *
from Instantiation import *
from Operation import *

app = Flask(__name__)

def find_val(child):
    if child.n_lefts == 0 and child.n_rights == 0:
        return child
    else:
        for chld in child.children:
            return find_val(chld) 

nlp = spacy.load('en')

def parse_line(text_in):
    new_line, types = replace(text_in)
    sents = nlp(" ".join(new_line))
    word_info = []
    for word in nltk.pos_tag(nltk.word_tokenize(" ".join(new_line))):
        word_info.append({"word": word[0]})
        word_info[-1]["pos"] = word[1]

    for index, token in enumerate(sents):
        word_info[index]["rel"] = token.dep_
        word_info[index]["children"] = token.children
    
    return word_info, types

def create_tree_node(word_info, op_info):
    key_words = {"assign", "plus", "minus", "multiply", "divide", "loop", "is", "in" "put"}
    math_terms = {"plus", "minus", "multiply", "divide"}
    curr_statement = Statement()
    while op_info:
        curr_obj = None
        math = False
        loop = False
        pos_look = ""
        curr_type = ""
        curr_type = op_info[0]
        if 'loop' in op_info:
            curr_statement.type = StmtType.LOOP
            op_info.remove("loop")
            pos_look = ["JJR", "JJ", "JJS"]
            curr_type = "loop"
            curr_obj = Operation()
        elif curr_type in math_terms:
            math = True
            if not curr_statement.type:
                curr_statement.type = StmtType.OP
            if curr_statement.type == StmtType.INST:
                curr_statement.type = StmtType.INST_DEF
            op_info.remove(curr_type)
            pos_look = ["CC", "VB"]
            curr_obj = Operation()
        elif "assignment" in op_info and len(op_info) == 1:
            if not curr_statement.type:
                curr_statement.type = StmtType.INST 
            else:
                curr_statement.type = StmtType.INST_DEF
            curr_type = "assign"
            op_info.remove("assignment")
            curr_obj = Instantiation()
        else:
            op_info.reverse()
            continue
        for index, word in enumerate(word_info):
            if (curr_type != "loop" and word["word"] == curr_type) or (curr_type == "loop" and word["pos"] in pos_look and word["word"] != curr_type):
                if math or curr_type == "loop":
                    curr_obj.set_type(word["word"], "not" in op_info)
                    if "not" in op_info:
                        op_info.remove("not")
                item_1 = None
                item_2 = None
                count = 1
                remove_list = []
                count1 = 0;
                count2 = 0;
                while (not item_1 or not item_2) and (not item_2 and index+count < len(word_info) or (not item_1 and  index-count >= 0)):
                    if index + count < len(word_info) and not item_2:
                        pos = word_info[index + count]["pos"]
                        rel = word_info[index + count]["rel"]
                        word = word_info[index + count]["word"]
                        if (pos == "CD" or pos == "DT" or pos == "VB" or pos == "NNP" or pos == "NN" or pos== "NNS" or rel[1:] == "obj" or rel == "punct") and word not in key_words:
                            item_2 = word_info[index + count]["word"]
                            remove_list.append(word_info[index + count])
                            count1 = count+1
                    if index - count >= 0 and not item_1:
                        pos = word_info[index - count]["pos"]
                        rel = word_info[index - count]["rel"]
                        word = word_info[index - count]["word"]
                        if (pos == "CD" or pos == "DT" or pos == "VB" or pos == "NNP" or pos == "NN" or pos== "NNS" or rel[1:] == "obj" or rel == "punct") and word not in key_words:
                            item_1 = word_info[index - count]["word"]
                            remove_list.append(word_info[index - count])
                            count2 = count+1
                    count+=1
                if not item_1 or not item_2:
                    while not item_1 and index + count1 < len(word_info):
                        pos = word_info[index + count1]["pos"]
                        rel = word_info[index + count1]["rel"]
                        word = word_info[index + count1]["word"]
                        if (pos == "CD" or pos == "DT" or pos == "NNP" or pos == "VB" or pos == "NN" or pos== "NNS" or rel[1:] == "obj" or rel == "punct") and word not in key_words:
                            item_1 = word_info[index + count1]["word"]
                            remove_list.append(word_info[index + count1])
                        count1+=1
                    while not item_2 and index - count2 >= 0:
                        pos = word_info[index - count2]["pos"]
                        rel = word_info[index - count2]["rel"]
                        word = word_info[index - count2]["word"]
                        if (pos == "CD" or pos == "DT" or pos == "NNP" or pos == "NN" or pos == "VB" or pos== "NNS" or rel[1:] == "obj" or rel == "punct") and word not in key_words:
                            item_2 = word_info[index - count2]["word"]
                            remove_list.append(word_info[index - count2])
                        count2+=1
                        
                for item in remove_list:
                    word_info.remove(item)
 
                curr_obj.left = item_1
                curr_obj.right = item_2
 
                break 
            
        if curr_type == "loop":
            curr_statement.condition = curr_obj        
            
        elif curr_type in math_terms:
            curr_statement.operation = curr_obj
   
        elif curr_type == "assign":
            curr_statement.instantiation = curr_obj

    return curr_statement

def operation_convert(operation):
    output = ""
    if operation.op == OpType.LT:
        output += operation.left + " < " + operation.right
    elif operation.op == OpType.GT:
        output += operation.left + " > " + operation.right
    elif operation.op == OpType.EQ:
        output += operation.left + " == " + operation.right
    elif operation.op == OpType.NEQ:
        output += operation.left + " != " + operation.right
    elif operation.op == OpType.ADD:
        output += operation.left + " + " + operation.right
    elif operation.op == OpType.SUB:
        output += operation.left + " - " + operation.right
    elif operation.op == OpType.MUL:
        output += operation.left + " * " + operation.right
    elif operation.op == OpType.DIV:
        output += operation.left + " - " + operation.right
    return output  

def instantiation_convert(tree):
    output = ""
    if tree.instantiation.left:
        if not tree.instantiation.left.isdigit():
            output+=tree.instantiation.left+" = "
            if tree.instantiation.right:
                output+=tree.instantiation.right
            else:
                output += "None"
        else:
            output+=tree.instantiation.right+" = "+tree.instantiation.left
    else:
        output+=tree.instantiation.right+" = None"
    return output

def definition_instantiation(tree):
    output = ""
    if tree.instantiation.left:
        output += tree.instantiation.left+ " = "
    else:
        output += tree.instantiation.right+ " = "
    output += operation_convert(tree.operation)
    return output

def convert_to_code(tree):
    output = ""
    while tree:
        if tree.type == StmtType.INST:
            output += instantiation_convert(tree)
        elif tree.type == StmtType.INST_DEF:
            output += definition_instantiation(tree)
        elif tree.type == StmtType.OP:
            if tree.operation.left.isdigit():
                output += tree.operation.right + " = "
            else:    
                output += tree.operation.left + " = "
            output += operation_convert(tree.operation)
        elif tree.type == StmtType.LOOP:
            output += "while "+operation_convert(tree.condition)+":\n"
            output += "\t"+tree.operation.left + " = "+operation_convert(tree.operation)
        output += "\n"
        tree = tree.next 
    return output 

@app.route('/speakcompiler', methods=['POST'])
def main():
    start = None
    end = None
    text_vals = request.get_json()
    code_text = text_vals["text"].split("\n")
    for line in code_text:
        word_info, op_info = parse_line(line)
        statement = create_tree_node(word_info, op_info)
        if not start:
            start = statement
            end = statement
        else:
            end.next = statement
            end = statement
    results = convert_to_code(start)
    response = app.response_class(response = results, status=200,mimetype="text/html")
    return response

if __name__ == '__main__':
    app.run(debug=False, use_reloader=True)
