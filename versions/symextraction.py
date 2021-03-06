def main(args):    
	x, y, z = symbols('x y z')
	expr = 2*x**4 + x**3 + 5*x**2 + 7*x + 11
	expp = math(args["eqn"])

	stack = []
	coef = ["f", "e", "d", "c", "b", "a"]
	d = {}
	export = []

	for arg in postorder_traversal(expp):
		temp = ""
		if( isinstance(arg, Integer) or isinstance(arg, Symbol) ):
			stack.append(arg)
		elif(isinstance(arg, Rational)):
			temp = ""
			temp = "(" + str(arg) + ")"
			stack.append(temp)
		elif( isinstance(arg, Mul)):
			mlen = len(arg.args)
			temp = ""
			for i in range(mlen):
				if( i == 0 ):
					x = stack.pop()
					if ( isinstance(x, Integer)) :
						substitute = coef.pop()
						temp = substitute
						d.update({substitute:int(x)})
					else:
						temp = str(x)
				else:
					x = stack.pop()
					if ( isinstance(x, Integer)) :
						substitute = coef.pop()
						temp = substitute + "*" + temp
						d.update({substitute:int(x)})
					else:
						temp = str(x) + "*" + temp

			stack.append(temp)
		elif( isinstance(arg, Add)):
			alen = len(arg.args)
			temp = ""
			for i in range(alen):
				if( i == 0 ):
					x = stack.pop()
					if ( isinstance(x, Integer)) :
						substitute = coef.pop()
						temp = substitute
						d.update({substitute:int(x)})
					else:
						temp = str(x)
				else:
					x = stack.pop()
					if ( isinstance(x, Integer)) :
						substitute = coef.pop()
						temp = substitute + " + " + temp
						d.update({substitute:int(x)})
					else:
						temp = str(x) + " + " + temp

			stack.append(temp)
		elif( isinstance(arg, Pow)):
			plen = len(arg.args)
			temp = ""
			for i in range(plen):
				if( i == 0 ):
					temp = str(stack.pop())
				else:
					temp = str(stack.pop()) + "**" + temp
			stack.append(temp)
		else:
			temp = str(arg.func)
			temp = temp + "(" + str(stack.pop()) + ")"
			stack.append(temp)


	temp = str(stack.pop())
	return { "jsready": temp, "jsonarray": d }