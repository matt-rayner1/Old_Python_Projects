import secrets
import string

alphabet = string.ascii_letters + string.digits + "!\"£$%^&*()_+-=`|\\/\'@~{}[];:<>,.?"

file1 = open("strings.txt", "w")

for i in range(10):
  while True:
    password = "".join(secrets.choice(alphabet) for i in range(12))
    if( any(c.islower() for c in password) 
		and any(c.isupper() for c in password) 
		and any(c.isdigit() for c in password)):
      break
  print(password)
  file1.write(password + "\n")