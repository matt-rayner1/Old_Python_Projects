import appex
import clipboard
import random

def main():
	text = appex.get_text()
	if text:
		list1 = list(text.lower())
		for i in range(len(list1)):
			if random.randint(0,1):
				list1[i] = list1[i].upper()
		clipboard.set("".join(list1))
		print("".join(list1))
	else:
		print('No input text found.')

if __name__ == '__main__':
	main()
