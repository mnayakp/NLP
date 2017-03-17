import sys

def compute(bin_str):
	if (int(bin_str,2) >= 0x00) & (int(bin_str,2) <= 0x7F):
		bin_str_new = "0" + bin_str[9:]
		
	elif (int(bin_str,2) >= 0x80) & (int(bin_str,2) <= 0x7FF):
		bin_str_new = "110" + bin_str[5:10] + "10" + bin_str[10:]	
	
	elif (int(bin_str,2) >= 0x800) & (int(bin_str,2) <= 0xFFFF):
		bin_str_new =  "1110" + bin_str[0:4] +  "10" + bin_str[4:10] +  "10" + bin_str[10:] 
	
	return bin_str_new


def main():
	filename = sys.argv[1]
	f = open(filename,"rb")
	byte_result = f.read()
	f.close()

	L = [byte_result[i:i+1] for i in range(len(byte_result))]
	binary_result = ""
	for i in L:
		binary_result = binary_result + '{0:08b}'.format(ord(i))
	
	
	result_string = ""
	binary_string_code_point = [binary_result[j:j+16] for j in range(0,len(binary_result),16)]
	for i in binary_string_code_point:
		result = compute(i)
		result_string += result
		

	final_result = []
	file_output = open('utf8encoder_out.txt' , 'wb')
	for i in range(0,len(result_string),8):
		final_result.append(int(result_string[i:i+8],2))
	file_output.write(bytes(final_result))
	file_output.close()

	
if __name__ == "__main__": main()
