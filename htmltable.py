import argparse
import sys

def tablegenerate(input, output, format, separate):
	print("\n------JOB START------\n")
	data = []
	if input == "":
		str = (sys.stdin.readline())[:-1]
		while str != "q":
			data.append(str.split(separate))
			str = sys.stdin.readline()[:-1]
	else:
		with open(input) as readfile:
			for line in readfile:
				line = line[:-1] if line[-1] == '\n' else line
				data.append(line.split(separate))
	writer = open(output, 'w') if output != "" else sys.stdout
	writer.write({'l': '\\[\\begin{bmatrix}\n', 'h': '<table>\n', 'm':''}[format])
	
	writer.write({'l':'\t', 'h':'\t<tr>\n\t\t<th>', 'm':'| '}[format])
	writer.write(({'l': ' & ', 'h':'</th><th>', 'm': ' | '}[format]).join(data[0]))
	writer.write({'l':' \\\\\n', 'h':'<th>\n\t<tr>\n', 'm':' |\n'}[format])
	if format == 'm':
		line = '| '
		for cell in data[0]:
			line += '--- | '
		writer.write(line + '\n')
		
	for i in range(len(data)):
		writer.write({'l':'\t', 'h':'\t<tr>\n\t\t<td>', 'm':'| '}[format])
		writer.write(({'l': ' & ', 'h':'</td><td>', 'm': ' | '}[format]).join(data[i]))
		writer.write({'l':'', 'h':'<td>\n\t<tr>\n', 'm':' |\n'}[format])
		if format == 'l':
			writer.write(' \\\\\n' if i != len(data) - 1 else '\n')
	
	writer.write({'l': '\\end{bmatrix}\\]\n', 'h': '<\\table>\n', 'm':'\n'}[format])
	writer.close()
	print('\n------JOB FINISH' + (' OUTPUT: '+output if output != "" else '') + '------')	
	
	
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Convert input to a formatted table, \
	default from stdin to stdout formatted in HTML table, seperated by space',
	conflict_handler='resolve')
	parser.add_argument("-i", help="File name of the input", metavar='input')
	parser.add_argument("-o", help="File name of the output", metavar='output')
	parser.add_argument("-f", help="Output format, l for LaTeX matrix, \
	h for HTML table, m for markdown table", metavar='format')
	parser.add_argument("-d", help="symbol that separate data cell")
	args = parser.parse_args()
	format = args.f if args.f is not None and args.f in ['l', 'h', 'm'] else 'h'
	input = args.i if args.i is not None else ""
	output = args.o if args.o is not None else ""
	separate = args.d if args.d is not None else " "
	
	tablegenerate(input, output, format, separate)


	
	
# def tablegenerate(fileInput, fileOutput, header):
	# print('------JOB START------\n')
	# if len(fileInput) <= 5 or fileInput[-4:] != '.csv':
		# print('Invalid input filename: ' + fileInput)
		# exit(1)
	# csvfile = open(fileInput, 'r')
	# reader = csv.reader(csvfile, delimiter=',')
	# textfile = open(fileOutput, 'w') if fileOutput != sys.stdout else sys.stdout
	# textfile.write('<table>\n')
	# for row in reader:
		# textfile.write('\t<tr>\n\t\t')
		# for cell in row:
			# if header:
				# textfile.write('<th>'+str(cell)+'</th>')
			# else:
				# textfile.write('<td>'+str(cell)+'</td>')
		# header = False
		# textfile.write('\n\t</tr>\n')
	# textfile.write('</table>\n')
	
	# print('\n------JOB FINISH' + (' , Output in file'+fileOutput if fileOutput != sys.stdout else '') + '------')	
			
		

