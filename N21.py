import itertools
import random
import string
 
bad_symbols = '1IlOo0'
uppercase_ = list(filter((lambda x: x not in bad_symbols),string.ascii_uppercase))
lowercase_ = list(filter((lambda x: x not in bad_symbols),string.ascii_lowercase))
digits_ = list(filter((lambda x: x not in bad_symbols),string.digits))

def generate_password(m):

	min_ = 1
	max_ = m-2
	u = random.randint(1,max_)
	
	max_ = m - u - 1
	d = random.randint(1,max_)

	l = m - u - d

	result = [random.choice(uppercase_) for i in range(u)] 
	result += [random.choice(lowercase_) for i in range(l)] 
	result += [random.choice(digits_) for i in range(d)] 
	random.shuffle(result)
	result = ''.join(result)
	return result
 
def main(n,m):
	z = set()
	while len(z) < n:
		z.add(generate_password(m))
	return list(z)

#print("Случайный пароль из 7 символов:" , generate_password(7))
print("10 случайных паролей длиной 15 символов:")
print(*main(10, 15), sep="\n")
