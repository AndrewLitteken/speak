#!/usr/bin/env python2.7

import sys

def replace(string):
	addSet = ["+", "sum", "plus", "add", "and", "total", "increased", "raise", "combined", "all", "altogether", "together", "both", "added", "increment", "append", "combine", "count", "summate", "addition"]

	subtractSet = ["-", "decrease", "decreased", "difference", "reduce", "lost", "left", "remainder", "remainder", "remaining", "diminished", "subtract", "subtracted", "deduct", "detract", "diminish", "remove", "take", "withdraw", "knock", "off", "out", "minus"]

	multiplySet = ["*", "multiply", "multiplied", "times", "per", "twice", "by", "area", "volume", "product", "apiece", "doubled", "tripled", "quadrupled", "compound", "cube", "double", "produce", "square", "repeat"]

	divideSet = ["/", "divide", "divided", "quotient", "split", "cut", "piece", "average", "ratio", "shared", "part", "break", "bisect", "dissect", "halve", "intersect", "quarter", "section", "segment"]

	loopSet = ["loop", "looped", "again", "while", "for", "repeat", "range", "from", "looping", "repeated"]

	equalCompSet = ["==", "equal", "same", "identical", "twin", "compare", "compared", "equivalent", "match", "matching", "duplicate", "look-alike", "matched", "like", "parallel", "even", "homologous", "identic", "indistinguishable", "tantamount"]

	unequalCompSet = ["!=", "differing", "uneven", "disparate", "dissimilar", "distant", "divergent", "diverse", "icommensurate", "mismatched", "odd", "unalike", "unequivalent", "unlike", "unmatched", "unsimilar", "varying", "weird", "not"]

	aroundSet = ["around", "round", "rounded", "close", "about", "almost"]

	variableSet = ["var", "int", "variable", "number", "string", "integer", "thing", "object", "word", "digit", "character", "something", "counter"]
	
	words = string.strip().split(" ")
	operations = []
	for i, word in enumerate(words):
		w = word.lower()
		if w in set(addSet):
			words[i] = "plus"
			operations.append("add")
		if w in set(subtractSet):
			words[i] = "minus"
			operations.append("subtract")
		if w in set(multiplySet):
			words[i] = "multiply"
			operations.append("multiply")
		if w in set(divideSet):
			words[i] = "divide"
		if w in set(loopSet):
			words[i] = "loop"
			operations.append("loop")
		if w in set(equalCompSet):
			operations.append("equalcompare")
		if w in set(unequalCompSet):
			operations.append("unequalcompare")
		if w in set(aroundSet):
			words[i] = "rounded"
		if w in set(variableSet):
			words.remove(word)
		if w == "equals":
			operations.append("assignment")

	if "unequalcompare" in [a for a in words]:
		try:
			words.remove("equalcompare")
		except:
			pass
	print words
	print operations

for line in sys.stdin:
	replace(line)
