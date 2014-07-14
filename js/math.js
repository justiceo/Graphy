// JavaScript Document
//gets a, b and c from form input and solves
function quad_num() {    
	
	var a, b, c, x1, x2;
	a = document.getElementById("a").value;
	b = document.getElementById("b").value;
	c = document.getElementById("c").value;
		
	solve(a,b,c);
	
}

//extracts a, b and c from an expression and solves
function quad_eqn() {
	
	var str = document.getElementById("eqn").value;
	var a, b, c, x1, x2, coef, numbers;	
	numbers = str.match(/-?\d/gi);	//get all the numbers
	
	
	numbers = numbers.toString();
	var num = numbers.split(",");
	if ( num.length > 3 ) {
		a = num[0];
		b = num[2]
		c = num[3];
	}
	else {
		a = 1;
		b = num[1];
		c = num[2];
	}
	
	//treat the -1 cases
	as = str.match(/-{1}\w{1}[^]/gi);	//get the case in the form of -x2 instead of -1x2
	if(as){
		a = -1;
		alert(as);
	}
	bs = str.match(/-{1}\w{1}[-+]/gi);	//get the case in the form of -x instead of -1x
	if(bs) {
		b = -1;
		alert(bs);
	}
	
	solve(a,b,c);
}

//the quadratic formular - processes the three values
function solve(a,b,c) {
	
	var x1 = ( -b - Math.sqrt( b*b - 4*a*c )) / ( 2*a );
	var x2 = ( -b + Math.sqrt( b*b - 4*a*c )) / ( 2*a );
	
	document.getElementById("solution").innerHTML = "solution:<br /> x = " + x1 + ", " + x2 + ". ";
}
	