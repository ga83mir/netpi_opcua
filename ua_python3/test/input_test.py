from __future__ import print_function
import sys
import time


def main():
	while True:
		try:
			a = input("input True: ")
		except NameError:
			sys.stdout.write('\x1b[1A')
			sys.stdout.write('\x1b[2K')
			#sys.stdout.flush()
			print("press True")
			time.sleep(1)
                        sys.stdout.write('\x1b[1A')
                        sys.stdout.write('\x1b[2K')
			#print("'\x1b[2K'")
			#sys.stdout.write("Please press True \r")
		else:
			break

if __name__=="__main__":
	main()
