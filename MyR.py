import ply.lex as lex
import ply.yacc as yacc
import sys

# Definicion de los Tokens y palabras reservadas
reserved = {
	'program' : 'PROGRAM',
	'main' : 'MAIN',
	'vars' : 'VARS',
	'function' : 'FUNCTION',
	'return' : 'RETURN',
	'read' : 'READ',
	'write' : 'WRITE',
	'if' : 'IF',
	'else' : 'ELSE',
	'while' : 'WHILE',
	'for' : 'FOR',
	'then' : 'THEN',
	'to' : 'TO',
	'do' : 'DO',
	'void' : 'VOID',
	'int' : 'INT',
	'float' : 'FLOAT',
	'char'	:	'CHAR',
	'media' : 'MEDIA',
	'moda' : 'MODA',
	'varianza' : 'VARIANZA',
	'regSim' : 'REGSIM',
	'plot' : 'PLOT' 
}
tokens = [ 'NUM_I', 'NUM_F', 'ID', 'PLUS', 'MINUS', 'MULT', 'DIV', 'LPAR', 'RPAR',
			'LBRA', 'RBRA', 'EQUAL', 'SCO', 'COM', 'LT', 'MT', 'NOTEQUAL', 
			'STRING', 'LCOR', 'RCOR', 'CR', 'AND', 'OR', 'EEQ', 'DP'] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULT = r'\*'
t_DIV = r'\/'
t_LPAR = r'\('
t_RPAR = r'\)'
t_LBRA = r'\{'
t_RBRA = r'\}'
t_EQUAL = r'\='
t_SCO = r'\;'
t_COM = r'\,'
t_LT = r'\<'
t_MT = r'\>'
t_NOTEQUAL = r'\!='
t_LCOR = r'\['
t_RCOR = r'\]'
t_AND = r'\&'
t_OR = r'\|'
t_EEQ = r'\=='
t_DP = r'\:'

t_ignore = ' \t'

def t_NUM_F(t):
	r'\d+\.\d+'
	t.value = float(t.value)
	return t
	
def t_NUM_I(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_CR(t): 
	r'\'[a-zA-Z]\''
	t.type = 'CR'
	return t

def t_ID(t): 
	r'[a-zA-Z_]([a-zA-Z]| \d+)*'
	if t.value in reserved:
		t.type = reserved[t.value]    # lista de palabras reservadas
	return t

def t_STRING(t): 
	r'%%([^\\"\n]+|\\.)*'
	t.type = 'STRING'
	return t

#Saltos de linea
def t_newLine(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

#Funcino que maneja caracteres extraños
def t_error(t):
	print("Ilegal charcater '%s'" % t.value[0])
	t.lexer.skip(1)
	
lexer = lex.lex()

#Parser (definicion de la gramatica)

def p_PROGRAMA(p):
	'''PROGRAMA : PROGRAM ID SCO VARIABLES FUNCIONES BLOQUE
				| PROGRAM ID SCO FUNCIONES BLOQUE
				| PROGRAM ID SCO VARIABLES BLOQUE
				| PROGRAM ID SCO BLOQUE'''
				
def p_VARIABLES(p):
	'''VARIABLES : VARS TIPO DP OTRA'''
				
def p_OTRA(p):
	'''OTRA : ID OTRA
			| ID LCOR NUM_I RCOR OTRA
			| TIPO DP OTRA
			| COM OTRA
			| SCO OTRA
			| empty'''
	
#vacios
def p_empty(p):
	'empty :'
	pass
						
def p_TIPO(P):
	'''TIPO : INT
			| FLOAT 
			| CHAR'''
			
def p_FUNCIONES(p):
	'''FUNCIONES : FUNCTION TIPO ID LPAR OTRA RPAR VARIABLES LBRA ESTATUTOS RBRA
                | FUNCTION TIPO ID LPAR OTRA RPAR LBRA ESTATUTOS  RBRA
				| FUNCTION VOID ID LPAR OTRA RPAR VARIABLES LBRA ESTATUTOS RBRA
				| FUNCTION VOID ID LPAR OTRA RPAR LBRA ESTATUTOS RBRA'''
	
def p_BLOQUE(p):
	'''BLOQUE : MAIN LPAR RPAR LBRA ESTATUTOS RBRA'''
	
def p_ESTATUTOS(p):
	'''ESTATUTOS : EST ESTATUTOS
				| empty'''
				
def p_EST(p): 
	'''EST : ASIGNACION
			| LECTURA
			| RETORNO
			| ESCRITURA
			| DESICION
			| CONDICIONAL
			| NOCONDICIONAL
			| LLAMADA'''
			
def p_ASIGNACION(p):
	'''ASIGNACION : ID LCOR EXPRESION RCOR EQUAL EXPRESION SCO
                    | ID EQUAL ID LPAR EXPRESION RPAR SCO
					| ID EQUAL EXPRESION SCO'''
				
def p_LECTURA(p):
	'''LECTURA : READ LPAR OTRA RPAR SCO'''
	
def p_RETORNO(p):
	'''RETORNO : RETURN LPAR EXPRESION RPAR SCO'''
	
def p_ESCRITURA(p):
	'''ESCRITURA : WRITE LPAR LETRERO RPAR SCO'''
	
def p_LETRERO(p):
	'''LETRERO : STRING LETRERO
            | EXPRESION LETRERO 
			| ID LETRERO 
			| COM LETRERO 
			| empty'''
			
def p_DESICION(p):
	'''DESICION : IF LPAR EXPRESION RPAR THEN LBRA ESTATUTOS RBRA ELSE LBRA ESTATUTOS RBRA
	            | IF LPAR EXPRESION RPAR THEN LBRA ESTATUTOS RBRA'''
				
def p_CONDICIONAL(p):
	'''CONDICIONAL : WHILE LPAR EXPRESION RPAR DO LBRA ESTATUTOS RBRA'''
	
def p_NOCONDICIONAL(p):
	'''NOCONDICIONAL : FOR ID EQUAL EXPRESION TO EXPRESION DO LBRA ESTATUTOS RBRA'''
	
def p_LLAMADA(p): 
	'''LLAMADA : ID LPAR OTRA RPAR SCO'''
	
def p_EXPRESION(p):
	'''EXPRESION : EXP SIM EXP 
				| EXP'''
				
def p_SIM(p):
	'''SIM : LT 
			| MT
			| NOTEQUAL
			| EEQ
			| AND
			| OR'''
			
def p_EXP(p):
	'''EXP : TERMINO PLUS TERMINO
			| TERMINO MINUS TERMINO
			| TERMINO'''

def p_TERMINO(p):
	'''TERMINO : FACTOR MULT FACTOR
				| FACTOR DIV FACTOR
				| FACTOR'''
				
def p_FACTOR(p):
	'''FACTOR : LPAR EXP2 RPAR 
			| LCOR EXP RCOR
			| LPAR EXP RPAR
			| CONSTANTE'''
			
def p_EXP2(p):
	'''EXP2 : EXP EXP2
			| COM EXP2 
			| empty'''
			
def p_CONSTANTE(p):
	'''CONSTANTE : ID
	            | NUM_I
				| NUM_F
				| CR'''

#Manejo de errores en el sintaxis
def p_error(p):
	if p == None:
		t = "EOF"
	else:
		t = f"{p.type}({p.value}) on line {p.lineno}"
	print(f"Syntax error: {t}")
	
parser = yacc.yacc()

with open(r'prueba.txt','r') as file:
	try:
		print("Parsing Complete")
		ast = parser.parse(file.read())
		print(ast)
	except:
		print("Error while reading the file")