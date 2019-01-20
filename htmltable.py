import csv
import sys

def tablegenerate(fileInput, fileOutput, header):
	print('------JOB START------\n')
	if len(fileInput) <= 5 or fileInput[-4:] != '.csv':
		print('Invalid input filename: ' + fileInput)
		exit(1)
	csvfile = open(fileInput, 'r')
	reader = csv.reader(csvfile, delimiter=',')
	textfile = open(fileOutput, 'w') if fileOutput != sys.stdout else sys.stdout
	textfile.write('<table>\n')
	for row in reader:
		textfile.write('\t<tr>\n\t\t')
		for cell in row:
			if header:
				textfile.write('<th>'+str(cell)+'</th>')
			else:
				textfile.write('<td>'+str(cell)+'</td>')
		header = False
		textfile.write('\n\t</tr>\n')
	textfile.write('</table>\n')
	
	print('\n------JOB FINISH' + (' , Output in file'+fileOutput if fileOutput != sys.stdout else '') + '------')	
			
if __name__ == "__main__":
	header = False
	fileInput = sys.stdin
	fileOutput = sys.stdout
	if len(sys.argv) >= 2:
		fileInput = sys.argv[1]
		if len(sys.argv) >= 3:
			fileOutput = sys.argv[2]
		if len(sys.argv) >= 4:
			header = sys.argv[3] in ['T', 't', '1', 'True', 'true']
		tablegenerate(fileInput, fileOutput, header)
	# if len(sys.argv) >= 4:
	else: 
		print("usage: in_csv_file_name out_txt_file_name header")