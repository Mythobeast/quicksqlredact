import sys

import sqlparse

PRETABLES = ['FROM', 'INTO', 'UPDATE']

def replace_names():
	with open(sys.argv[1], 'r') as infile:
		content = infile.readlines()
	content = '\n'.join(content)

	with open(sys.argv[2], 'r') as infile:
		replacements = infile.readlines()

	for row in replacements:
		source, target = row.split(',')
		content = content.replace(source,target)
	writepath = sys.argv[1] + '.out'

	with open(writepath, 'w') as outfile:
		outfile.write(content)

def extract_name_list():
	with open(sys.argv[1], 'r') as infile:
		content = infile.readlines()
	allsql = ' '.join(content)
	statementlist = sqlparse.split(allsql)
	tablenameset = set()
	columnnameset = set()
	pretable = False
	for statement in statementlist:
		parsed = sqlparse.parse(statement)
		for token in parsed.tokens:
			if token.ttype == Token.Name:
				if pretable:
					tablenameset.add(token.name)
				else:
					columnnameset.add(token.name)
				pretable = False
			elif token.ttype == Keyword and token.name.upper() in PRETABLES:
				pretable = True
			else:
				pretable = False


	tablenamelist = list(tablenameset).sort()
	columnnamelist = list(tablenameset).sort()
	writepath = sys.argv[1] + '.list'
	with open(writepath, 'w') as outfile:
		counter = 1
		for onename in tablenamelist:
			outfile.write(f"{onename},onetable{counter:02}\n")
		counter = 1
		for onename in columnnamelist:
			outfile.write(f"{onename},onetable{counter:03}\n")


def main():
	if len(sys.argv) == 2:
		extract_name_list()
	elif len(sys.argv) == 3:
		replace_names()



