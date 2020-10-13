import ply.lex as lex
import ply.yacc as yacc
import sys

tokens = [
    'RTHEN',
    'CONJ',
    'DISJ',
    'LBRACKET',
    'RBRACKET',
    'ID',
    'DOT'
]

t_ID = r'[a-z_A-Z][a-z_A-Z0-9]*'
t_RTHEN = r'\:\-'
t_CONJ = r'\,'
t_DISJ = r'\;'
t_LBRACKET = r'\('
t_RBRACKET = r'\)'
t_DOT = r'\.'

t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def t_error(t):
    raise SyntaxError


def t_eof(t):
    return None


lexer = lex.lex()


def p_program(p):
    '''program : program relation
               | relation '''
    if len(p) == 3:
        p[0] = p[1] + '\n' + p[2]
    elif len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ""


def p_relation(p):
    '''relation : head RTHEN body DOT
                | head DOT'''
    if len(p) == 5:
        p[0] = "Rel(" + p[1] + ", " + p[3] + ")"
    else:
        p[0] = "Rel(" + p[1] + ")"


def p_head(p):
    'head : atom'
    p[0] = "Head(" + p[1] + ")"


def p_atom(p):
    '''atom : ID
            | ID atom_close'''
    if len(p) == 2:
        p[0] = "ID(" + p[1] + ")"
    elif len(p) == 3:
        p[0] = "Atom(ID(" + p[1] + "), " + p[2] + ")"


def p_atom_in_gen(p):
    'atom_in_gen :  LBRACKET atom_in RBRACKET'
    p[0] = "Atom(" + p[2] + ")"


def p_atom_in1(p):
    'atom_in : LBRACKET atom_in RBRACKET'
    p[0] = p[2]


def p_atom_in2(p):
    '''atom_in : ID
               | ID atom_close'''
    if len(p) == 2:
        p[0] = "ID(" + p[1] + ")"
    else:
        p[0] = "ID(" + p[1] + "), " + p[2]


def p_atom_close1(p):
    '''atom_close : ID
                  | ID atom_close'''
    if len(p) == 2:
        p[0] = "ID(" + p[1] + ")"
    else:
        p[0] = "ID(" + p[1] + "), " + p[2]


def p_atom_close2(p):
    '''atom_close : atom_in_gen
                  | atom_in_gen atom_close'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + ", " + p[2]


def p_body(p):
    'body : disj'
    p[0] = "Body(" + p[1] + ")"


def p_disj(p):
    '''disj : conj
            | conj DISJ disj'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = "Disj(" + p[1] + ", " + p[3] + ")"


def p_conj(p):
    '''conj : lit
            | lit CONJ conj'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = "Conj(" + p[1] + ", " + p[3] + ")"


def p_lit(p):
    '''lit : LBRACKET disj RBRACKET
           | atom'''
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_error(p):
    raise SyntaxError


parser = yacc.yacc()


def parse(file):
    with open(file, "r") as f:
        data = f.read()
    tree = parser.parse(data)
    resfile = open(file + '.out', 'w')
    resfile.write(str(tree))


if __name__ == "__main__":
    filename = sys.argv[1]
    try:
        parse(filename)
    except SyntaxError:
        print("Unable to parse")
