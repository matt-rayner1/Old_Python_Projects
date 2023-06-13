#I'm sorry.

def text_to_owo(text):
	vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
	smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']
	
	text = text.replace('L', 'W').replace('l', 'w')
	text = text.replace('R', 'W').replace('r', 'w')
	
	text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
	text = last_replace(text, '?', '? owo')
	text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))
	
	for v in vowels:
		if 'n{}'.format(v) in text:
			text = text.replace('n{}'.format(v), 'ny{}'.format(v))
			if 'N{}'.format(v) in text:
				text = text.replace('N{}'.format(v), 'N{}{}'.format('Y' if v.isupper() else 'y', v))
	return text
	
def main():	
	texty_wexty = appex.get_text()
	
	if texty_wexty:
		texty_wexty = text_to_owo(texty_wexty)
		texty_wexty = texty_wexty.replace("uck", "ucky wucky")
		clipboard.set(texty_wexty)
		print(texty_wexty)
	else:
		print('No input text found.')

if __name__ == '__main__':
	main()
