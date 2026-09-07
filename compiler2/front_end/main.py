import re
# ==========================================
# 1. ANALISADOR LÉXICO (LEXER)
# ==========================================
TOKEN_TYPES = [
    ('<?php', r'<\?php'),
    ('?>', r'\?>'),
    ('if', r'\bif\b'),
    ('else', r'\belse\b'),
    ('while', r'\bwhile\b'),
    ('echo', r'\becho\b'),
    # Note que floatval e readline foram separados conforme a nova tabela
    ('floatval', r'\bfloatval\b'),
    ('readline', r'\breadline\b'),
    ('PHP_EOL', r'\bPHP_EOL\b'),
    ('numero_real', r'\d+(\.\d+)?'),
    ('$id', r'\$[a-zA-Z_][a-zA-Z0-9_]*'),
    ('==', r'=='), ('!=', r'!='), ('>=', r'>='), ('<=', r'<='),
    ('>', r'>'), ('<', r'<'),
    ('=', r'='),
    ('+', r'\+'), ('-', r'-'), ('*', r'\*'), ('/', r'/'),
    ('.', r'\.'), (',', r','), (';', r';'),
    ('(', r'\('), (')', r'\)'), ('{', r'\{'), ('}', r'\}'),
    ('WS', r'\s+'),
]

# Compilação prévia para performance
COMPILED_TOKENS = [
    (token_type, re.compile(regex))
    for token_type, regex in TOKEN_TYPES
]

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.pos = 0
        self.tokenize()

    def tokenize(self):
        pos = 0
        while pos < len(self.code):
            match = None
            for token_type, pattern in COMPILED_TOKENS:
                match = pattern.match(self.code, pos)
                if match:
                    if token_type != 'WS':
                        self.tokens.append({'classe': token_type, 'lexema': match.group(0)})
                    pos = match.end()
                    break
            if not match:
                print(f"Erro Léxico: Caractere inválido: {self.code[pos]}")
                break
        self.tokens.append({'classe': '$', 'lexema': 'EOF'})

    def next_token(self):
        if self.pos < len(self.tokens):
            t = self.tokens[self.pos]
            self.pos += 1
            return t
        return {'classe': '$', 'lexema': 'EOF'}

    def print_tokens(self):
        print(self.tokens)

# ==========================================
# 2. REGRAS DA GRAMÁTICA (LHS, |RHS|)
# ==========================================
# ATUALIZADO: O tamanho a desempilhar (|RHS|) agora reflete os tokens soltos.
REGRAS = {
    0: ("PROG'", 1),
    1: ("PROG", 3),
    2: ("DC", 2),
    3: ("VAR", 1),
    4: ("VARS", 2),
    5: ("MAIS_VAR", 2),
    6: ("MAIS_VAR", 0),
    7: ("CMDS", 2),
    8: ("CMDS", 2),
    9: ("CMDS", 1),
    10: ("CMDS", 0),
    11: ("MAIS_CMDS", 2),
    12: ("CMD_COND", 8),     # if ( CONDICAO ) { CMDS } PFALSA -> 8 tokens!
    13: ("CMD_COND", 7),     # while ( CONDICAO ) { CMDS } -> 7 tokens!
    14: ("CMD", 4),
    15: ("CMD", 2),
    16: ("PFALSA", 4),       # else { CMDS } -> 4 tokens!
    17: ("PFALSA", 0),
    18: ("RESTO_IDENT", 2),
    19: ("EXP_IDENT", 1),
    20: ("EXP_IDENT", 6),    # floatval ( readline ( ) ) -> 6 tokens!
    21: ("CONDICAO", 3),
    22: ("RELACAO", 1),
    23: ("RELACAO", 1),
    24: ("RELACAO", 1),
    25: ("RELACAO", 1),
    26: ("RELACAO", 1),
    27: ("RELACAO", 1),
    28: ("EXPRESSAO", 2),
    29: ("TERMO", 3),
    30: ("OP_UN", 1),
    31: ("OP_UN", 0),
    32: ("FATOR", 1),
    33: ("FATOR", 1),
    34: ("FATOR", 3),
    35: ("OUTROS_TERMOS", 3),
    36: ("OUTROS_TERMOS", 0),
    37: ("OP_AD", 1),
    38: ("OP_AD", 1),
    39: ("MAIS_FATORES", 3),
    40: ("MAIS_FATORES", 0),
    41: ("OP_MUL", 1),
    42: ("OP_MUL", 1)
}

# ==========================================
# 3. TABELAS LR(1) (AÇÕES E GOTOS)
# ==========================================
# Geradas baseadas no arquivo "tabela.xlsx" com 146 estados
ACTION = {
    (0, '<?php'): 'S2',
    (1, '$'): 'ACC',
    (2, '$id'): 'S8',
    (2, '?>'): 'R10',
    (2, 'echo'): 'S7',
    (2, 'if'): 'S9',
    (2, 'while'): 'S10',
    (3, '?>'): 'S13',
    (4, ';'): 'S15',
    (5, '$id'): 'S8',
    (5, '?>'): 'R10',
    (5, 'echo'): 'S7',
    (5, 'if'): 'S9',
    (5, 'while'): 'S10',
    (6, '?>'): 'R9',
    (7, '$id'): 'S17',
    (8, ','): 'S21',
    (8, ';'): 'R6',
    (8, '='): 'S20',
    (9, '('): 'S22',
    (10, '('): 'S23',
    (11, ';'): 'S15',
    (12, ';'): 'R3',
    (13, '$'): 'R1',
    (14, '?>'): 'R7',
    (15, '$id'): 'S8',
    (15, '?>'): 'R10',
    (15, 'echo'): 'S7',
    (15, 'if'): 'S9',
    (15, 'while'): 'S10',
    (16, '?>'): 'R8',
    (17, '.'): 'S26',
    (18, ';'): 'R15',
    (19, ';'): 'R4',
    (20, '$id'): 'R31',
    (20, '('): 'R31',
    (20, '-'): 'S32',
    (20, 'floatval'): 'S29',
    (20, 'numero_real'): 'R31',
    (21, '$id'): 'S34',
    (22, '$id'): 'R31',
    (22, '('): 'R31',
    (22, '-'): 'S32',
    (22, 'numero_real'): 'R31',
    (23, '$id'): 'R31',
    (23, '('): 'R31',
    (23, '-'): 'S32',
    (23, 'numero_real'): 'R31',
    (24, '?>'): 'R2',
    (25, '?>'): 'R11',
    (26, 'PHP_EOL'): 'S40',
    (27, ';'): 'R18',
    (28, ';'): 'R19',
    (29, '('): 'S41',
    (30, '+'): 'S44',
    (30, '-'): 'S45',
    (30, ';'): 'R36',
    (31, '$id'): 'S47',
    (31, '('): 'S49',
    (31, 'numero_real'): 'S48',
    (32, '$id'): 'R30',
    (32, '('): 'R30',
    (32, 'numero_real'): 'R30',
    (33, ';'): 'R5',
    (34, ','): 'S21',
    (34, ';'): 'R6',
    (35, ')'): 'S50',
    (36, '!='): 'S53',
    (36, '<'): 'S57',
    (36, '<='): 'S55',
    (36, '=='): 'S52',
    (36, '>'): 'S56',
    (36, '>='): 'S54',
    (37, '!='): 'R36',
    (37, '+'): 'S60',
    (37, '-'): 'S61',
    (37, '<'): 'R36',
    (37, '<='): 'R36',
    (37, '=='): 'R36',
    (37, '>'): 'R36',
    (37, '>='): 'R36',
    (38, '$id'): 'S63',
    (38, '('): 'S65',
    (38, 'numero_real'): 'S64',
    (39, ')'): 'S66',
    (40, ';'): 'R14',
    (41, 'readline'): 'S67',
    (42, ';'): 'R28',
    (43, '$id'): 'R31',
    (43, '('): 'R31',
    (43, '-'): 'S32',
    (43, 'numero_real'): 'R31',
    (44, '$id'): 'R37',
    (44, '('): 'R37',
    (44, '+'): 'R37',
    (44, '-'): 'R37',
    (44, ';'): 'R37',
    (44, 'numero_real'): 'R37',
    (45, '$id'): 'R38',
    (45, '('): 'R38',
    (45, '+'): 'R38',
    (45, '-'): 'R38',
    (45, ';'): 'R38',
    (45, 'numero_real'): 'R38',
    (46, '*'): 'S71',
    (46, '+'): 'R40',
    (46, '-'): 'R40',
    (46, '/'): 'S72',
    (46, ';'): 'R40',
    (47, '*'): 'R32',
    (47, '+'): 'R32',
    (47, '-'): 'R32',
    (47, '/'): 'R32',
    (47, ';'): 'R32',
    (48, '*'): 'R33',
    (48, '+'): 'R33',
    (48, '-'): 'R33',
    (48, '/'): 'R33',
    (48, ';'): 'R33',
    (49, '$id'): 'R31',
    (49, '('): 'R31',
    (49, '-'): 'S32',
    (49, 'numero_real'): 'R31',
    (50, '{'): 'S76',
    (51, '$id'): 'R31',
    (51, '('): 'R31',
    (51, '-'): 'S32',
    (51, 'numero_real'): 'R31',
    (52, '$id'): 'R22',
    (52, '('): 'R22',
    (52, ')'): 'R22',
    (52, '+'): 'R22',
    (52, '-'): 'R22',
    (52, 'numero_real'): 'R22',
    (53, '$id'): 'R23',
    (53, '('): 'R23',
    (53, ')'): 'R23',
    (53, '+'): 'R23',
    (53, '-'): 'R23',
    (53, 'numero_real'): 'R23',
    (54, '$id'): 'R24',
    (54, '('): 'R24',
    (54, ')'): 'R24',
    (54, '+'): 'R24',
    (54, '-'): 'R24',
    (54, 'numero_real'): 'R24',
    (55, '$id'): 'R25',
    (55, '('): 'R25',
    (55, ')'): 'R25',
    (55, '+'): 'R25',
    (55, '-'): 'R25',
    (55, 'numero_real'): 'R25',
    (56, '$id'): 'R26',
    (56, '('): 'R26',
    (56, ')'): 'R26',
    (56, '+'): 'R26',
    (56, '-'): 'R26',
    (56, 'numero_real'): 'R26',
    (57, '$id'): 'R27',
    (57, '('): 'R27',
    (57, ')'): 'R27',
    (57, '+'): 'R27',
    (57, '-'): 'R27',
    (57, 'numero_real'): 'R27',
    (58, '!='): 'R28',
    (58, '<'): 'R28',
    (58, '<='): 'R28',
    (58, '=='): 'R28',
    (58, '>'): 'R28',
    (58, '>='): 'R28',
    (59, '$id'): 'R31',
    (59, '('): 'R31',
    (59, '-'): 'S32',
    (59, 'numero_real'): 'R31',
    (60, '!='): 'R37',
    (60, '$id'): 'R37',
    (60, '('): 'R37',
    (60, '+'): 'R37',
    (60, '-'): 'R37',
    (60, '<'): 'R37',
    (60, '<='): 'R37',
    (60, '=='): 'R37',
    (60, '>'): 'R37',
    (60, '>='): 'R37',
    (60, 'numero_real'): 'R37',
    (61, '!='): 'R38',
    (61, '$id'): 'R38',
    (61, '('): 'R38',
    (61, '+'): 'R38',
    (61, '-'): 'R38',
    (61, '<'): 'R38',
    (61, '<='): 'R38',
    (61, '=='): 'R38',
    (61, '>'): 'R38',
    (61, '>='): 'R38',
    (61, 'numero_real'): 'R38',
    (62, '!='): 'R40',
    (62, '*'): 'S71',
    (62, '+'): 'R40',
    (62, '-'): 'R40',
    (62, '/'): 'S72',
    (62, '<'): 'R40',
    (62, '<='): 'R40',
    (62, '=='): 'R40',
    (62, '>'): 'R40',
    (62, '>='): 'R40',
    (63, '!='): 'R32',
    (63, '*'): 'R32',
    (63, '+'): 'R32',
    (63, '-'): 'R32',
    (63, '/'): 'R32',
    (63, '<'): 'R32',
    (63, '<='): 'R32',
    (63, '=='): 'R32',
    (63, '>'): 'R32',
    (63, '>='): 'R32',
    (64, '!='): 'R33',
    (64, '*'): 'R33',
    (64, '+'): 'R33',
    (64, '-'): 'R33',
    (64, '/'): 'R33',
    (64, '<'): 'R33',
    (64, '<='): 'R33',
    (64, '=='): 'R33',
    (64, '>'): 'R33',
    (64, '>='): 'R33',
    (65, '$id'): 'R31',
    (65, '('): 'R31',
    (65, '-'): 'S32',
    (65, 'numero_real'): 'R31',
    (66, '{'): 'S82',
    (67, '('): 'S83',
    (68, '+'): 'S44',
    (68, '-'): 'S45',
    (68, ';'): 'R36',
    (69, '+'): 'R29',
    (69, '-'): 'R29',
    (69, ';'): 'R29',
    (70, '$id'): 'S47',
    (70, '('): 'S49',
    (70, 'numero_real'): 'S48',
    (71, '$id'): 'R41',
    (71, '('): 'R41',
    (71, 'numero_real'): 'R41',
    (72, '$id'): 'R42',
    (72, '('): 'R42',
    (72, 'numero_real'): 'R42',
    (73, ')'): 'S86',
    (74, ')'): 'R36',
    (74, '+'): 'S89',
    (74, '-'): 'S90',
    (75, '$id'): 'S92',
    (75, '('): 'S94',
    (75, 'numero_real'): 'S93',
    (76, '$id'): 'S8',
    (76, 'echo'): 'S7',
    (76, 'if'): 'S99',
    (76, 'while'): 'S100',
    (76, '}'): 'R10',
    (77, ')'): 'R21',
    (78, '!='): 'R36',
    (78, '+'): 'S60',
    (78, '-'): 'S61',
    (78, '<'): 'R36',
    (78, '<='): 'R36',
    (78, '=='): 'R36',
    (78, '>'): 'R36',
    (78, '>='): 'R36',
    (79, '!='): 'R29',
    (79, '+'): 'R29',
    (79, '-'): 'R29',
    (79, '<'): 'R29',
    (79, '<='): 'R29',
    (79, '=='): 'R29',
    (79, '>'): 'R29',
    (79, '>='): 'R29',
    (80, '$id'): 'S63',
    (80, '('): 'S65',
    (80, 'numero_real'): 'S64',
    (81, ')'): 'S104',
    (82, '$id'): 'S8',
    (82, 'echo'): 'S7',
    (82, 'if'): 'S99',
    (82, 'while'): 'S100',
    (82, '}'): 'R10',
    (83, ')'): 'S106',
    (84, ';'): 'R35',
    (85, '*'): 'S71',
    (85, '+'): 'R40',
    (85, '-'): 'R40',
    (85, '/'): 'S72',
    (85, ';'): 'R40',
    (86, '*'): 'R34',
    (86, '+'): 'R34',
    (86, '-'): 'R34',
    (86, '/'): 'R34',
    (86, ';'): 'R34',
    (87, ')'): 'R28',
    (88, '$id'): 'R31',
    (88, '('): 'R31',
    (88, '-'): 'S32',
    (88, 'numero_real'): 'R31',
    (89, '$id'): 'R37',
    (89, '('): 'R37',
    (89, ')'): 'R37',
    (89, '+'): 'R37',
    (89, '-'): 'R37',
    (89, 'numero_real'): 'R37',
    (90, '$id'): 'R38',
    (90, '('): 'R38',
    (90, ')'): 'R38',
    (90, '+'): 'R38',
    (90, '-'): 'R38',
    (90, 'numero_real'): 'R38',
    (91, ')'): 'R40',
    (91, '*'): 'S71',
    (91, '+'): 'R40',
    (91, '-'): 'R40',
    (91, '/'): 'S72',
    (92, ')'): 'R32',
    (92, '*'): 'R32',
    (92, '+'): 'R32',
    (92, '-'): 'R32',
    (92, '/'): 'R32',
    (93, ')'): 'R33',
    (93, '*'): 'R33',
    (93, '+'): 'R33',
    (93, '-'): 'R33',
    (93, '/'): 'R33',
    (94, '$id'): 'R31',
    (94, '('): 'R31',
    (94, '-'): 'S32',
    (94, 'numero_real'): 'R31',
    (95, '}'): 'S112',
    (96, ';'): 'S114',
    (97, '$id'): 'S8',
    (97, 'echo'): 'S7',
    (97, 'if'): 'S99',
    (97, 'while'): 'S100',
    (97, '}'): 'R10',
    (98, '}'): 'R9',
    (99, '('): 'S116',
    (100, '('): 'S117',
    (101, ';'): 'S114',
    (102, '!='): 'R35',
    (102, '<'): 'R35',
    (102, '<='): 'R35',
    (102, '=='): 'R35',
    (102, '>'): 'R35',
    (102, '>='): 'R35',
    (103, '!='): 'R40',
    (103, '*'): 'S71',
    (103, '+'): 'R40',
    (103, '-'): 'R40',
    (103, '/'): 'S72',
    (103, '<'): 'R40',
    (103, '<='): 'R40',
    (103, '=='): 'R40',
    (103, '>'): 'R40',
    (103, '>='): 'R40',
    (104, '!='): 'R34',
    (104, '*'): 'R34',
    (104, '+'): 'R34',
    (104, '-'): 'R34',
    (104, '/'): 'R34',
    (104, '<'): 'R34',
    (104, '<='): 'R34',
    (104, '=='): 'R34',
    (104, '>'): 'R34',
    (104, '>='): 'R34',
    (105, '}'): 'S120',
    (106, ')'): 'S121',
    (107, '+'): 'R39',
    (107, '-'): 'R39',
    (107, ';'): 'R39',
    (108, ')'): 'R36',
    (108, '+'): 'S89',
    (108, '-'): 'S90',
    (109, ')'): 'R29',
    (109, '+'): 'R29',
    (109, '-'): 'R29',
    (110, '$id'): 'S92',
    (110, '('): 'S94',
    (110, 'numero_real'): 'S93',
    (111, ')'): 'S124',
    (112, '$id'): 'R17',
    (112, '?>'): 'R17',
    (112, 'echo'): 'R17',
    (112, 'else'): 'S126',
    (112, 'if'): 'R17',
    (112, 'while'): 'R17',
    (113, '}'): 'R7',
    (114, '$id'): 'S8',
    (114, 'echo'): 'S7',
    (114, 'if'): 'S99',
    (114, 'while'): 'S100',
    (114, '}'): 'R10',
    (115, '}'): 'R8',
    (116, '$id'): 'R31',
    (116, '('): 'R31',
    (116, '-'): 'S32',
    (116, 'numero_real'): 'R31',
    (117, '$id'): 'R31',
    (117, '('): 'R31',
    (117, '-'): 'S32',
    (117, 'numero_real'): 'R31',
    (118, '}'): 'R2',
    (119, '!='): 'R39',
    (119, '+'): 'R39',
    (119, '-'): 'R39',
    (119, '<'): 'R39',
    (119, '<='): 'R39',
    (119, '=='): 'R39',
    (119, '>'): 'R39',
    (119, '>='): 'R39',
    (120, '$id'): 'R13',
    (120, '?>'): 'R13',
    (120, 'echo'): 'R13',
    (120, 'if'): 'R13',
    (120, 'while'): 'R13',
    (121, ';'): 'R20',
    (122, ')'): 'R35',
    (123, ')'): 'R40',
    (123, '*'): 'S71',
    (123, '+'): 'R40',
    (123, '-'): 'R40',
    (123, '/'): 'S72',
    (124, ')'): 'R34',
    (124, '*'): 'R34',
    (124, '+'): 'R34',
    (124, '-'): 'R34',
    (124, '/'): 'R34',
    (125, '$id'): 'R12',
    (125, '?>'): 'R12',
    (125, 'echo'): 'R12',
    (125, 'if'): 'R12',
    (125, 'while'): 'R12',
    (126, '{'): 'S131',
    (127, '}'): 'R11',
    (128, ')'): 'S132',
    (129, ')'): 'S133',
    (130, ')'): 'R39',
    (130, '+'): 'R39',
    (130, '-'): 'R39',
    (131, '$id'): 'S8',
    (131, 'echo'): 'S7',
    (131, 'if'): 'S99',
    (131, 'while'): 'S100',
    (131, '}'): 'R10',
    (132, '{'): 'S135',
    (133, '{'): 'S136',
    (134, '}'): 'S137',
    (135, '$id'): 'S8',
    (135, 'echo'): 'S7',
    (135, 'if'): 'S99',
    (135, 'while'): 'S100',
    (135, '}'): 'R10',
    (136, '$id'): 'S8',
    (136, 'echo'): 'S7',
    (136, 'if'): 'S99',
    (136, 'while'): 'S100',
    (136, '}'): 'R10',
    (137, '$id'): 'R16',
    (137, '?>'): 'R16',
    (137, 'echo'): 'R16',
    (137, 'if'): 'R16',
    (137, 'while'): 'R16',
    (138, '}'): 'S140',
    (139, '}'): 'S141',
    (140, '$id'): 'R17',
    (140, 'echo'): 'R17',
    (140, 'else'): 'S143',
    (140, 'if'): 'R17',
    (140, 'while'): 'R17',
    (140, '}'): 'R17',
    (141, '$id'): 'R13',
    (141, 'echo'): 'R13',
    (141, 'if'): 'R13',
    (141, 'while'): 'R13',
    (141, '}'): 'R13',
    (142, '$id'): 'R12',
    (142, 'echo'): 'R12',
    (142, 'if'): 'R12',
    (142, 'while'): 'R12',
    (142, '}'): 'R12',
    (143, '{'): 'S144',
    (144, '$id'): 'S8',
    (144, 'echo'): 'S7',
    (144, 'if'): 'S99',
    (144, 'while'): 'S100',
    (144, '}'): 'R10',
    (145, '}'): 'S146',
    (146, '$id'): 'R16',
    (146, 'echo'): 'R16',
    (146, 'if'): 'R16',
    (146, 'while'): 'R16',
    (146, '}'): 'R16'
}

GOTO = {
    (0, 'PROG'): 1,
    (2, 'CMD'): 4,
    (2, 'CMDS'): 3,
    (2, 'CMD_COND'): 5,
    (2, 'DC'): 6,
    (2, 'VAR'): 11,
    (2, 'VARS'): 12,
    (4, 'MAIS_CMDS'): 14,
    (5, 'CMD'): 4,
    (5, 'CMDS'): 16,
    (5, 'CMD_COND'): 5,
    (5, 'DC'): 6,
    (5, 'VAR'): 11,
    (5, 'VARS'): 12,
    (8, 'MAIS_VAR'): 19,
    (8, 'RESTO_IDENT'): 18,
    (11, 'MAIS_CMDS'): 24,
    (15, 'CMD'): 4,
    (15, 'CMDS'): 25,
    (15, 'CMD_COND'): 5,
    (15, 'DC'): 6,
    (15, 'VAR'): 11,
    (15, 'VARS'): 12,
    (20, 'EXPRESSAO'): 28,
    (20, 'EXP_IDENT'): 27,
    (20, 'OP_UN'): 31,
    (20, 'TERMO'): 30,
    (21, 'VARS'): 33,
    (22, 'CONDICAO'): 35,
    (22, 'EXPRESSAO'): 36,
    (22, 'OP_UN'): 38,
    (22, 'TERMO'): 37,
    (23, 'CONDICAO'): 39,
    (23, 'EXPRESSAO'): 36,
    (23, 'OP_UN'): 38,
    (23, 'TERMO'): 37,
    (30, 'OP_AD'): 43,
    (30, 'OUTROS_TERMOS'): 42,
    (31, 'FATOR'): 46,
    (34, 'MAIS_VAR'): 19,
    (36, 'RELACAO'): 51,
    (37, 'OP_AD'): 59,
    (37, 'OUTROS_TERMOS'): 58,
    (38, 'FATOR'): 62,
    (43, 'OP_UN'): 31,
    (43, 'TERMO'): 68,
    (46, 'MAIS_FATORES'): 69,
    (46, 'OP_MUL'): 70,
    (49, 'EXPRESSAO'): 73,
    (49, 'OP_UN'): 75,
    (49, 'TERMO'): 74,
    (51, 'EXPRESSAO'): 77,
    (51, 'OP_UN'): 75,
    (51, 'TERMO'): 74,
    (59, 'OP_UN'): 38,
    (59, 'TERMO'): 78,
    (62, 'MAIS_FATORES'): 79,
    (62, 'OP_MUL'): 80,
    (65, 'EXPRESSAO'): 81,
    (65, 'OP_UN'): 75,
    (65, 'TERMO'): 74,
    (68, 'OP_AD'): 43,
    (68, 'OUTROS_TERMOS'): 84,
    (70, 'FATOR'): 85,
    (74, 'OP_AD'): 88,
    (74, 'OUTROS_TERMOS'): 87,
    (75, 'FATOR'): 91,
    (76, 'CMD'): 96,
    (76, 'CMDS'): 95,
    (76, 'CMD_COND'): 97,
    (76, 'DC'): 98,
    (76, 'VAR'): 101,
    (76, 'VARS'): 12,
    (78, 'OP_AD'): 59,
    (78, 'OUTROS_TERMOS'): 102,
    (80, 'FATOR'): 103,
    (82, 'CMD'): 96,
    (82, 'CMDS'): 105,
    (82, 'CMD_COND'): 97,
    (82, 'DC'): 98,
    (82, 'VAR'): 101,
    (82, 'VARS'): 12,
    (85, 'MAIS_FATORES'): 107,
    (85, 'OP_MUL'): 70,
    (88, 'OP_UN'): 75,
    (88, 'TERMO'): 108,
    (91, 'MAIS_FATORES'): 109,
    (91, 'OP_MUL'): 110,
    (94, 'EXPRESSAO'): 111,
    (94, 'OP_UN'): 75,
    (94, 'TERMO'): 74,
    (96, 'MAIS_CMDS'): 113,
    (97, 'CMD'): 96,
    (97, 'CMDS'): 115,
    (97, 'CMD_COND'): 97,
    (97, 'DC'): 98,
    (97, 'VAR'): 101,
    (97, 'VARS'): 12,
    (101, 'MAIS_CMDS'): 118,
    (103, 'MAIS_FATORES'): 119,
    (103, 'OP_MUL'): 80,
    (108, 'OP_AD'): 88,
    (108, 'OUTROS_TERMOS'): 122,
    (110, 'FATOR'): 123,
    (112, 'PFALSA'): 125,
    (114, 'CMD'): 96,
    (114, 'CMDS'): 127,
    (114, 'CMD_COND'): 97,
    (114, 'DC'): 98,
    (114, 'VAR'): 101,
    (114, 'VARS'): 12,
    (116, 'CONDICAO'): 128,
    (116, 'EXPRESSAO'): 36,
    (116, 'OP_UN'): 38,
    (116, 'TERMO'): 37,
    (117, 'CONDICAO'): 129,
    (117, 'EXPRESSAO'): 36,
    (117, 'OP_UN'): 38,
    (117, 'TERMO'): 37,
    (123, 'MAIS_FATORES'): 130,
    (123, 'OP_MUL'): 110,
    (131, 'CMD'): 96,
    (131, 'CMDS'): 134,
    (131, 'CMD_COND'): 97,
    (131, 'DC'): 98,
    (131, 'VAR'): 101,
    (131, 'VARS'): 12,
    (135, 'CMD'): 96,
    (135, 'CMDS'): 138,
    (135, 'CMD_COND'): 97,
    (135, 'DC'): 98,
    (135, 'VAR'): 101,
    (135, 'VARS'): 12,
    (136, 'CMD'): 96,
    (136, 'CMDS'): 139,
    (136, 'CMD_COND'): 97,
    (136, 'DC'): 98,
    (136, 'VAR'): 101,
    (136, 'VARS'): 12,
    (140, 'PFALSA'): 142,
    (144, 'CMD'): 96,
    (144, 'CMDS'): 145,
    (144, 'CMD_COND'): 97,
    (144, 'DC'): 98,
    (144, 'VAR'): 101,
    (144, 'VARS'): 12
}


# ==========================================
# 4. MOTOR LR(1) COM ANALISADOR SEMÂNTICO
# ==========================================
class ParserLR1:
    def __init__(self, lexer, action_table, goto_table, regras):
        self.lexer = lexer
        self.action = action_table
        self.goto = goto_table
        self.regras = regras

        # TABELA DE SÍMBOLOS: O coração do Analisador Semântico
        self.tabela_simbolos = set()

    def parse(self):
        pilha_estados = [0]

        # Agora a pilha guarda dicionários para não perdermos o valor real do token
        # Ex: {'classe': '$id', 'lexema': '$x'}
        pilha_simbolos = []

        lookahead = self.lexer.next_token()

        while True:
            estado_atual = pilha_estados[-1]
            token_classe = lookahead['classe']

            chave = (estado_atual, token_classe)
            acao = self.action.get(chave)

            if not acao:
                print(f"\n[ERRO SINTÁTICO] Token inesperado '{lookahead['lexema']}' (Classe: {token_classe}) no estado {estado_atual}")
                return False

            if acao == 'ACC':
                print("\n[SUCESSO SINTÁTICO E SEMÂNTICO] O código fonte é válido!")
                print(f"Tabela de Símbolos Final: {self.tabela_simbolos}")
                return True

            elif acao.startswith('S'):
                # === SHIFT ===
                proximo_estado = int(acao[1:])
                pilha_estados.append(proximo_estado)

                # Empilhamos o objeto inteiro do token, preservando o lexema
                pilha_simbolos.append(lookahead)
                lookahead = self.lexer.next_token()

            elif acao.startswith('R'):
                # === REDUCE (AÇÃO SEMÂNTICA) ===
                id_regra = int(acao[1:])
                lhs, tamanho_rhs = self.regras[id_regra]

                # Vamos capturar os itens que estão sendo reduzidos da pilha
                # para podermos inspecionar os valores antes de descartá-los
                itens_reduzidos = pilha_simbolos[-tamanho_rhs:] if tamanho_rhs > 0 else []

                # --- INÍCIO DAS VALIDAÇÕES SEMÂNTICAS ---

                # Regra 4: VARS -> $id MAIS_VAR (Momento da DECLARAÇÃO)
                if id_regra == 4:
                    nome_var = itens_reduzidos[0]['lexema']
                    if nome_var in self.tabela_simbolos:
                        print(f"\n[ERRO SEMÂNTICO] A variável '{nome_var}' já foi declarada anteriormente.")
                        return False
                    self.tabela_simbolos.add(nome_var)
                    print(f"[SEMÂNTICA] Variável declarada com sucesso: {nome_var}")

                # Regra 14: CMD -> echo $id . PHP_EOL (Momento de USO no echo)
                elif id_regra == 14:
                    nome_var = itens_reduzidos[1]['lexema']
                    if nome_var not in self.tabela_simbolos:
                        print(f"\n[ERRO SEMÂNTICO] Uso de variável não declarada no echo: '{nome_var}'.")
                        return False

                # Regra 15: CMD -> $id RESTO_IDENT (Momento de ATRIBUIÇÃO, ex: $x = ...)
                elif id_regra == 15:
                    nome_var = itens_reduzidos[0]['lexema']
                    if nome_var not in self.tabela_simbolos:
                        print(f"\n[ERRO SEMÂNTICO] Tentativa de atribuir valor a uma variável não declarada: '{nome_var}'.")
                        return False

                # Regra 32: FATOR -> $id (Momento de USO MATEMÁTICO, ex: ... + $x)
                elif id_regra == 32:
                    nome_var = itens_reduzidos[0]['lexema']
                    if nome_var not in self.tabela_simbolos:
                        print(f"\n[ERRO SEMÂNTICO] A variável '{nome_var}' foi usada numa expressão sem ser declarada.")
                        return False

                # --- FIM DAS VALIDAÇÕES SEMÂNTICAS ---

                # Desempilha os estados e símbolos sintáticos normalmente
                for _ in range(tamanho_rhs):
                    pilha_estados.pop()
                    pilha_simbolos.pop()

                estado_base = pilha_estados[-1]
                proximo_estado = self.goto.get((estado_base, lhs))

                if proximo_estado is None:
                    print(f"\n[ERRO INTERNO] Transição GOTO indefinida para Estado Base: {estado_base}, Simbolo: '{lhs}'")
                    return False

                # Empilha o Não-Terminal reduzido
                # Como o Não-Terminal não tem um lexema literal do código fonte, deixamos None
                pilha_simbolos.append({'classe': lhs, 'lexema': None})
                pilha_estados.append(proximo_estado)


# ==========================================
# 5. EXECUÇÃO
# ==========================================
if __name__ == '__main__':

    f = open("codigo.php","r")
    codigo_fonte  = f.read()
    f.close()

    print(codigo_fonte)
    print("Iniciando o compilador LR(1)...")
    meu_lexer = Lexer(codigo_fonte)
    meu_parser = ParserLR1(meu_lexer, ACTION, GOTO, REGRAS)
    meu_lexer.print_tokens()
    meu_parser.parse()
