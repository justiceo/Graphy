def main(args):
    
	x, y, z = symbols('x y z')
	a, b, c, d, e, f, g, h, i, j, k, kkz = symbols('a b c d e f g h i j k kkz')
	kka, kkb, kkc, kkd, kke, kkf, kkg, kkh, kki, kkj, kkk, kkz = symbols('kka kkb kkc kkd kke kkf kkg kkh kki kkj kkk kkz')
	expp = "x**2 + 6*x*cos(x) + 9 + tan(x+3)"
	expp = math(args["eqn"])
	expp = sympify(expp)
	stack = []
	coef = ["$k", "$j", "$i", "$h", "$g", "$f", "$e", "$d", "$c", "$b", "$a"]
	d = {}
	id_stack = []
	single_arg = False
	single_letter = False
	single_pow = False
	int_present = False
	can_be_solved = "0"
	bounds_stack = []



	def stack_id(temp_str):
		temp_str = str(temp_str)
		for key in d:
			if( temp_str.find(key) != -1 ):
				temp_str = temp_str.replace(key, str(d[key]))

		temp_str = id_stack_clean(temp_str)
		id_stack.append(temp_str)

	'''clean for sympy comparison'''	
	def cleanx(temp_str):
		temp_str = str(temp_str)
		temp_str = temp_str.replace("$","")
		temp_str = sympify(temp_str)
		return temp_str

	def id_stack_clean(temp_str):
		temp_str = str(temp_str)
		temp_str = temp_str.replace("$","kk")
		temp_str = simplify(temp_str)
		temp_str = str(temp_str)
		temp_str = temp_str.replace("kk","$")
		return temp_str

	if(isinstance(expp, Symbol)):
		substitute = coef.pop()
		single_letter = substitute + "*" + str(expp)
		stack_id(single_letter) 
		d.update({substitute: int(1)})
	elif(isinstance(expp, Integer)):
		substitute = coef.pop()
		single_letter = substitute 
		stack_id(single_letter)
		d.update({substitute: str(expp)})
		bounds_stack.append(str(expp))
		
	elif(isinstance(expp, Rational)):
		substitute = coef.pop()
		single_letter = substitute
		stack_id(single_letter)
		d.update({substitute: str((expp).evalf(5))})
		bounds_stack.append(str(expp))
	
	elif(len(expp.args) == 1 ):
		single_arg = True
	elif(isinstance(expp, Pow)):
		single_pow = True

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
						stack_id(temp)
						d.update({substitute:int(x)})
						int_present = True
					else:
						temp = str(x)
				else:
					x = stack.pop()
					if ( isinstance(x, Integer)) :
						substitute = coef.pop()
						temp = substitute + "*" + temp
						stack_id(temp)
						d.update({substitute:int(x)})
						int_present = True
					else:
						temp = str(x) + "*" + temp
			if(int_present):
				stack.append(temp)
				int_present = False
			else:
				substitute = coef.pop()
				temp = substitute + "*" + temp
				stack_id(temp)
				d.update({substitute:int(1)})
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
						stack_id(temp)
						d.update({substitute:int(x)})
					else:
						testvar = cleanx(x)
						if( isinstance(testvar, Mul)):
							temp = str(x)
						else:
							substitute = coef.pop()
							temp = substitute + "*" + str(x)
							stack_id(temp)
							d.update({substitute: int(1)})
				else:
					x = stack.pop()
					if ( isinstance(x, Integer)) :
						substitute = coef.pop()
						temp = substitute + " + " + temp
						stack_id(temp)
						d.update({substitute:int(x)})
					else:
						testvar = cleanx(x)
						if( isinstance(testvar, Mul)):
							temp = str(x) + " + " + temp
						else:
							substitute = coef.pop()
							temp = substitute + "*" + str(x) + " + " + temp
							stack_id(temp)
							d.update({substitute: int(1)})		
			stack.append(temp)
		elif( isinstance(arg, Pow)):
			plen = len(arg.args)
			temp = ""
			for i in range(plen):
				if( i == 0 ):
					temp = str(stack.pop())
				else:
					temp = str(stack.pop()) + "**" + temp
			if(single_pow):
				substitute = coef.pop()
				temp = substitute + "*" + temp
				stack_id(temp)
				d.update({substitute: int(1)})
			stack.append(temp)
		else:
			temp = str(arg.func)
			x = stack.pop()
			if( isinstance(x, Symbol)):
				substitute = coef.pop()
				temp = temp + "(" + substitute + "*" + str(x) + ")"
				stack_id(temp)
				d.update({substitute: int(1)})
			elif( isinstance(x, Integer)):
				substitute = coef.pop()
				temp = temp + "(" + substitute + ")"
				stack_id(temp)
				d.update({substitute: int(x)})
			else:
				temp = temp + "(" + str(x) + ")"
				
			if(single_arg):
				substitute = coef.pop()
				temp = substitute + "*" + temp  
				stack_id(temp)
				d.update({substitute: int(1)})			
			
			stack.append(temp)

	if(single_letter):	
		temp = single_letter
	else:
		temp = str(stack.pop())
		if(Poly(expp).is_univariate):
			can_be_solved = "1"
			first_d = diff(expp)
			c_points = solve(first_d)
			pgen = Poly(expp).gen
			for cpoint in c_points:
				y_values = expp.subs(pgen, cpoint).evalf(5)
				y_values = str(y_values)
				bounds_stack.append(y_values)


	return { "jsready": temp, "jsonarray": json.dumps(d), "solvable": can_be_solved, "idStack": id_stack, "gbounds": bounds_stack }