
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "startnonassocIFxnonassocELSEnonassocEQLNEQGTGTELTLTEleft+-left/*rightUMINUSleftTRANSPOSEADDASSIGN ASSIGN BREAK CONTINUE DIVASSIGN DOTADD DOTDIV DOTMUL DOTSUB ELSE EQL EYE FLOATNUM FOR GT GTE ID IF INTNUM LT LTE MULTASSIGN NEQ ONES PRINT RETURN STR SUBASSIGN TRANSPOSE WHILE ZEROS\n        start : statements\n    \n        statements : statements_list\n    \n        statements_list : statements_list statement\n    \n        statements_list : statement\n    \n        statement : assignment ';'\n                  | print ';'\n                  | continue ';'\n                  | break ';'\n                  | return ';'\n                  | if\n                  | for\n                  | while\n                  | nested_statements\n    \n        for : FOR ID ASSIGN expression ':' expression nested\n    \n        while : WHILE condition nested\n    \n        break : BREAK\n    \n        return : RETURN expression\n    \n        continue : CONTINUE\n    \n        print : PRINT coma_separated\n    \n        coma_separated : coma_separated ',' expression\n    \n        coma_separated : expression\n    \n        assignment : ID assign_symbol expression\n    \n        assignment : ID slice assign_symbol expression\n    \n        assign_symbol : ASSIGN\n                      | SUBASSIGN\n                      | ADDASSIGN\n                      | DIVASSIGN\n                      | MULTASSIGN\n    \n        expression : built_in_function '(' expression_list ')'\n    \n        expression_list : expression_list ',' expression\n    \n        expression_list : expression\n    \n        expression : term\n    \n        expression : expression '+' term\n                   | expression '-' term\n                   | expression '/' term\n                   | expression '*' term\n    \n        expression : expression EQL term\n                   | expression NEQ term\n                   | expression GT term\n                   | expression GTE term\n                   | expression LT term\n                   | expression LTE term \n    \n        expression : '-' term %prec UMINUS\n    \n        expression : expression TRANSPOSE\n    \n        expression : ID dot_operation term\n    \n        expression : vector dot_operation term\n    \n         dot_operation : DOTADD\n                       | DOTSUB\n                       | DOTMUL\n                       | DOTDIV\n    \n        vector : '[' vector_contents ']'\n    \n        vector : '[' ']'\n    \n        vector_contents : vector_contents ',' vector_element\n    \n        vector_contents : vector_element\n    \n        vector_element : term\n    \n        slice : '[' slice_contents ']'\n    \n        slice_contents : slice_contents ',' range\n    \n        slice_contents : range\n    \n        range : expression ':' expression\n    \n        range : expression ':'\n    \n        range : ':' expression\n    \n        range : expression\n    \n        if : IF condition nested %prec IFx\n    \n        if : IF condition nested ELSE nested\n    \n        condition : '(' expression ')'\n    \n        nested : statement\n    \n        nested_statements : nested_empty\n                          | nested_statements_list\n    \n        nested_statements_list : '{' statements_list '}'\n    \n        nested_empty : '{' '}'\n    \n        term : '(' expression ')'\n    \n        term : vector\n    \n        term : INTNUM\n    \n        term : FLOATNUM\n    \n        term : STR\n    \n        term : ID\n    \n        built_in_function : EYE\n                          | ONES\n                          | ZEROS\n    "
    
_lr_action_items = {'ID':([0,3,4,10,11,12,13,15,18,20,22,23,24,25,26,27,28,29,30,31,33,34,35,36,37,38,42,43,44,45,46,50,51,52,53,55,56,58,59,60,62,66,67,68,69,70,71,72,73,74,75,76,77,78,79,81,82,83,84,85,86,87,88,89,91,94,95,97,98,99,102,103,106,107,108,109,110,111,112,113,114,115,118,119,120,121,122,123,124,128,129,131,132,134,135,],[14,14,-4,-10,-11,-12,-13,45,45,57,-67,-68,14,-3,-5,-6,-7,-8,-9,45,-24,-25,-26,-27,-28,45,45,-32,83,-76,-72,-73,-74,-75,83,14,45,14,-70,14,45,45,45,83,83,83,83,83,83,83,83,83,83,-44,45,-43,-72,-76,83,-47,-48,-49,-50,83,-52,-63,-66,45,-15,-69,45,45,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-71,-45,-46,-51,83,14,-65,-29,45,-64,45,14,-14,]),'PRINT':([0,3,4,10,11,12,13,22,23,24,25,26,27,28,29,30,43,45,46,50,51,52,55,58,59,60,78,81,82,83,91,94,95,98,99,106,107,108,109,110,111,112,113,114,115,118,119,120,121,123,124,128,131,134,135,],[15,15,-4,-10,-11,-12,-13,-67,-68,15,-3,-5,-6,-7,-8,-9,-32,-76,-72,-73,-74,-75,15,15,-70,15,-44,-43,-72,-76,-52,-63,-66,-15,-69,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-71,-45,-46,-51,15,-65,-29,-64,15,-14,]),'CONTINUE':([0,3,4,10,11,12,13,22,23,24,25,26,27,28,29,30,43,45,46,50,51,52,55,58,59,60,78,81,82,83,91,94,95,98,99,106,107,108,109,110,111,112,113,114,115,118,119,120,121,123,124,128,131,134,135,],[16,16,-4,-10,-11,-12,-13,-67,-68,16,-3,-5,-6,-7,-8,-9,-32,-76,-72,-73,-74,-75,16,16,-70,16,-44,-43,-72,-76,-52,-63,-66,-15,-69,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-71,-45,-46,-51,16,-65,-29,-64,16,-14,]),'BREAK':([0,3,4,10,11,12,13,22,23,24,25,26,27,28,29,30,43,45,46,50,51,52,55,58,59,60,78,81,82,83,91,94,95,98,99,106,107,108,109,110,111,112,113,114,115,118,119,120,121,123,124,128,131,134,135,],[17,17,-4,-10,-11,-12,-13,-67,-68,17,-3,-5,-6,-7,-8,-9,-32,-76,-72,-73,-74,-75,17,17,-70,17,-44,-43,-72,-76,-52,-63,-66,-15,-69,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-71,-45,-46,-51,17,-65,-29,-64,17,-14,]),'RETURN':([0,3,4,10,11,12,13,22,23,24,25,26,27,28,29,30,43,45,46,50,51,52,55,58,59,60,78,81,82,83,91,94,95,98,99,106,107,108,109,110,111,112,113,114,115,118,119,120,121,123,124,128,131,134,135,],[18,18,-4,-10,-11,-12,-13,-67,-68,18,-3,-5,-6,-7,-8,-9,-32,-76,-72,-73,-74,-75,18,18,-70,18,-44,-43,-72,-76,-52,-63,-66,-15,-69,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-71,-45,-46,-51,18,-65,-29,-64,18,-14,]),'IF':([0,3,4,10,11,12,13,22,23,24,25,26,27,28,29,30,43,45,46,50,51,52,55,58,59,60,78,81,82,83,91,94,95,98,99,106,107,108,109,110,111,112,113,114,115,118,119,120,121,123,124,128,131,134,135,],[19,19,-4,-10,-11,-12,-13,-67,-68,19,-3,-5,-6,-7,-8,-9,-32,-76,-72,-73,-74,-75,19,19,-70,19,-44,-43,-72,-76,-52,-63,-66,-15,-69,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-71,-45,-46,-51,19,-65,-29,-64,19,-14,]),'FOR':([0,3,4,10,11,12,13,22,23,24,25,26,27,28,29,30,43,45,46,50,51,52,55,58,59,60,78,81,82,83,91,94,95,98,99,106,107,108,109,110,111,112,113,114,115,118,119,120,121,123,124,128,131,134,135,],[20,20,-4,-10,-11,-12,-13,-67,-68,20,-3,-5,-6,-7,-8,-9,-32,-76,-72,-73,-74,-75,20,20,-70,20,-44,-43,-72,-76,-52,-63,-66,-15,-69,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-71,-45,-46,-51,20,-65,-29,-64,20,-14,]),'WHILE':([0,3,4,10,11,12,13,22,23,24,25,26,27,28,29,30,43,45,46,50,51,52,55,58,59,60,78,81,82,83,91,94,95,98,99,106,107,108,109,110,111,112,113,114,115,118,119,120,121,123,124,128,131,134,135,],[21,21,-4,-10,-11,-12,-13,-67,-68,21,-3,-5,-6,-7,-8,-9,-32,-76,-72,-73,-74,-75,21,21,-70,21,-44,-43,-72,-76,-52,-63,-66,-15,-69,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-71,-45,-46,-51,21,-65,-29,-64,21,-14,]),'{':([0,3,4,10,11,12,13,22,23,24,25,26,27,28,29,30,43,45,46,50,51,52,55,58,59,60,78,81,82,83,91,94,95,98,99,106,107,108,109,110,111,112,113,114,115,118,119,120,121,123,124,128,131,134,135,],[24,24,-4,-10,-11,-12,-13,-67,-68,24,-3,-5,-6,-7,-8,-9,-32,-76,-72,-73,-74,-75,24,24,-70,24,-44,-43,-72,-76,-52,-63,-66,-15,-69,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-71,-45,-46,-51,24,-65,-29,-64,24,-14,]),'$end':([1,2,3,4,10,11,12,13,22,23,25,26,27,28,29,30,59,94,95,98,99,131,135,],[0,-1,-2,-4,-10,-11,-12,-13,-67,-68,-3,-5,-6,-7,-8,-9,-70,-63,-66,-15,-69,-64,-14,]),'}':([4,10,11,12,13,22,23,24,25,26,27,28,29,30,59,60,94,95,98,99,131,135,],[-4,-10,-11,-12,-13,-67,-68,59,-3,-5,-6,-7,-8,-9,-70,99,-63,-66,-15,-69,-64,-14,]),';':([5,6,7,8,9,16,17,39,40,43,45,46,50,51,52,54,61,78,81,82,83,91,100,105,106,107,108,109,110,111,112,113,114,115,118,119,120,121,128,],[26,27,28,29,30,-18,-16,-19,-21,-32,-76,-72,-73,-74,-75,-17,-22,-44,-43,-72,-76,-52,-23,-20,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-71,-45,-46,-51,-29,]),'ELSE':([10,11,12,13,22,23,26,27,28,29,30,59,94,95,98,99,131,135,],[-10,-11,-12,-13,-67,-68,-5,-6,-7,-8,-9,-70,123,-66,-15,-69,-64,-14,]),'ASSIGN':([14,32,57,101,],[33,33,97,-56,]),'SUBASSIGN':([14,32,101,],[34,34,-56,]),'ADDASSIGN':([14,32,101,],[35,35,-56,]),'DIVASSIGN':([14,32,101,],[36,36,-56,]),'MULTASSIGN':([14,32,101,],[37,37,-56,]),'[':([14,15,18,31,33,34,35,36,37,38,42,44,53,56,62,66,67,68,69,70,71,72,73,74,75,76,77,79,84,85,86,87,88,89,97,102,103,122,129,132,],[38,53,53,53,-24,-25,-26,-27,-28,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,53,-47,-48,-49,-50,53,53,53,53,53,53,53,]),'-':([15,18,31,33,34,35,36,37,38,40,42,43,45,46,50,51,52,54,56,61,62,65,66,67,78,79,80,81,82,83,91,96,97,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,120,121,125,127,128,129,132,133,134,],[44,44,44,-24,-25,-26,-27,-28,44,69,44,-32,-76,-72,-73,-74,-75,69,44,69,44,69,44,44,-44,44,69,-43,-72,-76,-52,69,44,69,44,44,69,69,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,69,-71,-45,-46,-51,69,69,-29,44,44,69,69,]),'EYE':([15,18,31,33,34,35,36,37,38,42,56,62,66,67,79,97,102,103,129,132,],[47,47,47,-24,-25,-26,-27,-28,47,47,47,47,47,47,47,47,47,47,47,47,]),'ONES':([15,18,31,33,34,35,36,37,38,42,56,62,66,67,79,97,102,103,129,132,],[48,48,48,-24,-25,-26,-27,-28,48,48,48,48,48,48,48,48,48,48,48,48,]),'ZEROS':([15,18,31,33,34,35,36,37,38,42,56,62,66,67,79,97,102,103,129,132,],[49,49,49,-24,-25,-26,-27,-28,49,49,49,49,49,49,49,49,49,49,49,49,]),'(':([15,18,19,21,31,33,34,35,36,37,38,41,42,44,47,48,49,53,56,62,66,67,68,69,70,71,72,73,74,75,76,77,79,84,85,86,87,88,89,97,102,103,122,129,132,],[42,42,56,56,42,-24,-25,-26,-27,-28,42,79,42,42,-77,-78,-79,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,-47,-48,-49,-50,42,42,42,42,42,42,42,]),'INTNUM':([15,18,31,33,34,35,36,37,38,42,44,53,56,62,66,67,68,69,70,71,72,73,74,75,76,77,79,84,85,86,87,88,89,97,102,103,122,129,132,],[50,50,50,-24,-25,-26,-27,-28,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,50,-47,-48,-49,-50,50,50,50,50,50,50,50,]),'FLOATNUM':([15,18,31,33,34,35,36,37,38,42,44,53,56,62,66,67,68,69,70,71,72,73,74,75,76,77,79,84,85,86,87,88,89,97,102,103,122,129,132,],[51,51,51,-24,-25,-26,-27,-28,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,51,-47,-48,-49,-50,51,51,51,51,51,51,51,]),'STR':([15,18,31,33,34,35,36,37,38,42,44,53,56,62,66,67,68,69,70,71,72,73,74,75,76,77,79,84,85,86,87,88,89,97,102,103,122,129,132,],[52,52,52,-24,-25,-26,-27,-28,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,52,-47,-48,-49,-50,52,52,52,52,52,52,52,]),':':([38,43,45,46,50,51,52,65,78,81,82,83,91,102,106,107,108,109,110,111,112,113,114,115,118,119,120,121,125,128,],[66,-32,-76,-72,-73,-74,-75,103,-44,-43,-72,-76,-52,66,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-71,-45,-46,-51,132,-29,]),',':([39,40,43,45,46,50,51,52,63,64,65,78,81,82,83,90,91,92,93,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,126,127,128,130,133,],[67,-21,-32,-76,-72,-73,-74,-75,102,-58,-62,-44,-43,-72,-76,122,-52,-54,-55,-60,-61,-20,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,129,-31,-71,-45,-46,-51,-57,-59,-29,-53,-30,]),'+':([40,43,45,46,50,51,52,54,61,65,78,80,81,82,83,91,96,100,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,120,121,125,127,128,133,134,],[68,-32,-76,-72,-73,-74,-75,68,68,68,-44,68,-43,-72,-76,-52,68,68,68,68,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,68,-71,-45,-46,-51,68,68,-29,68,68,]),'/':([40,43,45,46,50,51,52,54,61,65,78,80,81,82,83,91,96,100,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,120,121,125,127,128,133,134,],[70,-32,-76,-72,-73,-74,-75,70,70,70,-44,70,-43,-72,-76,-52,70,70,70,70,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,70,-71,-45,-46,-51,70,70,-29,70,70,]),'*':([40,43,45,46,50,51,52,54,61,65,78,80,81,82,83,91,96,100,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,120,121,125,127,128,133,134,],[71,-32,-76,-72,-73,-74,-75,71,71,71,-44,71,-43,-72,-76,-52,71,71,71,71,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,71,-71,-45,-46,-51,71,71,-29,71,71,]),'EQL':([40,43,45,46,50,51,52,54,61,65,78,80,81,82,83,91,96,100,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,120,121,125,127,128,133,134,],[72,-32,-76,-72,-73,-74,-75,72,72,72,-44,72,-43,-72,-76,-52,72,72,72,72,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,72,-71,-45,-46,-51,72,72,-29,72,72,]),'NEQ':([40,43,45,46,50,51,52,54,61,65,78,80,81,82,83,91,96,100,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,120,121,125,127,128,133,134,],[73,-32,-76,-72,-73,-74,-75,73,73,73,-44,73,-43,-72,-76,-52,73,73,73,73,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,73,-71,-45,-46,-51,73,73,-29,73,73,]),'GT':([40,43,45,46,50,51,52,54,61,65,78,80,81,82,83,91,96,100,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,120,121,125,127,128,133,134,],[74,-32,-76,-72,-73,-74,-75,74,74,74,-44,74,-43,-72,-76,-52,74,74,74,74,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,74,-71,-45,-46,-51,74,74,-29,74,74,]),'GTE':([40,43,45,46,50,51,52,54,61,65,78,80,81,82,83,91,96,100,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,120,121,125,127,128,133,134,],[75,-32,-76,-72,-73,-74,-75,75,75,75,-44,75,-43,-72,-76,-52,75,75,75,75,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,75,-71,-45,-46,-51,75,75,-29,75,75,]),'LT':([40,43,45,46,50,51,52,54,61,65,78,80,81,82,83,91,96,100,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,120,121,125,127,128,133,134,],[76,-32,-76,-72,-73,-74,-75,76,76,76,-44,76,-43,-72,-76,-52,76,76,76,76,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,76,-71,-45,-46,-51,76,76,-29,76,76,]),'LTE':([40,43,45,46,50,51,52,54,61,65,78,80,81,82,83,91,96,100,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,120,121,125,127,128,133,134,],[77,-32,-76,-72,-73,-74,-75,77,77,77,-44,77,-43,-72,-76,-52,77,77,77,77,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,77,-71,-45,-46,-51,77,77,-29,77,77,]),'TRANSPOSE':([40,43,45,46,50,51,52,54,61,65,78,80,81,82,83,91,96,100,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,120,121,125,127,128,133,134,],[78,-32,-76,-72,-73,-74,-75,78,78,78,-44,78,-43,-72,-76,-52,78,78,78,78,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,78,-71,-45,-46,-51,78,78,-29,78,78,]),']':([43,45,46,50,51,52,53,63,64,65,78,81,82,83,90,91,92,93,103,104,106,107,108,109,110,111,112,113,114,115,118,119,120,121,126,127,128,130,],[-32,-76,-72,-73,-74,-75,91,101,-58,-62,-44,-43,-72,-76,121,-52,-54,-55,-60,-61,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,-71,-45,-46,-51,-57,-59,-29,-53,]),')':([43,45,46,50,51,52,78,80,81,82,83,91,96,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,128,133,],[-32,-76,-72,-73,-74,-75,-44,118,-43,-72,-76,-52,124,-33,-34,-35,-36,-37,-38,-39,-40,-41,-42,128,-31,-71,-45,-46,-51,-29,-30,]),'DOTADD':([45,46,91,121,],[85,85,-52,-51,]),'DOTSUB':([45,46,91,121,],[86,86,-52,-51,]),'DOTMUL':([45,46,91,121,],[87,87,-52,-51,]),'DOTDIV':([45,46,91,121,],[88,88,-52,-51,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'start':([0,],[1,]),'statements':([0,],[2,]),'statements_list':([0,24,],[3,60,]),'statement':([0,3,24,55,58,60,123,134,],[4,25,4,95,95,25,95,95,]),'assignment':([0,3,24,55,58,60,123,134,],[5,5,5,5,5,5,5,5,]),'print':([0,3,24,55,58,60,123,134,],[6,6,6,6,6,6,6,6,]),'continue':([0,3,24,55,58,60,123,134,],[7,7,7,7,7,7,7,7,]),'break':([0,3,24,55,58,60,123,134,],[8,8,8,8,8,8,8,8,]),'return':([0,3,24,55,58,60,123,134,],[9,9,9,9,9,9,9,9,]),'if':([0,3,24,55,58,60,123,134,],[10,10,10,10,10,10,10,10,]),'for':([0,3,24,55,58,60,123,134,],[11,11,11,11,11,11,11,11,]),'while':([0,3,24,55,58,60,123,134,],[12,12,12,12,12,12,12,12,]),'nested_statements':([0,3,24,55,58,60,123,134,],[13,13,13,13,13,13,13,13,]),'nested_empty':([0,3,24,55,58,60,123,134,],[22,22,22,22,22,22,22,22,]),'nested_statements_list':([0,3,24,55,58,60,123,134,],[23,23,23,23,23,23,23,23,]),'assign_symbol':([14,32,],[31,62,]),'slice':([14,],[32,]),'coma_separated':([15,],[39,]),'expression':([15,18,31,38,42,56,62,66,67,79,97,102,103,129,132,],[40,54,61,65,80,96,100,104,105,117,125,65,127,133,134,]),'built_in_function':([15,18,31,38,42,56,62,66,67,79,97,102,103,129,132,],[41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,]),'term':([15,18,31,38,42,44,53,56,62,66,67,68,69,70,71,72,73,74,75,76,77,79,84,89,97,102,103,122,129,132,],[43,43,43,43,43,81,93,43,43,43,43,106,107,108,109,110,111,112,113,114,115,43,119,120,43,43,43,93,43,43,]),'vector':([15,18,31,38,42,44,53,56,62,66,67,68,69,70,71,72,73,74,75,76,77,79,84,89,97,102,103,122,129,132,],[46,46,46,46,46,82,82,46,46,46,46,82,82,82,82,82,82,82,82,82,82,46,82,82,46,46,46,82,46,46,]),'condition':([19,21,],[55,58,]),'slice_contents':([38,],[63,]),'range':([38,102,],[64,126,]),'dot_operation':([45,46,],[84,89,]),'vector_contents':([53,],[90,]),'vector_element':([53,122,],[92,130,]),'nested':([55,58,123,134,],[94,98,131,135,]),'expression_list':([79,],[116,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> statements','start',1,'p_start','Parser.py',34),
  ('statements -> statements_list','statements',1,'p_statements','Parser.py',41),
  ('statements_list -> statements_list statement','statements_list',2,'p_statements_list','Parser.py',48),
  ('statements_list -> statement','statements_list',1,'p_statements_list_single','Parser.py',56),
  ('statement -> assignment ;','statement',2,'p_statement','Parser.py',63),
  ('statement -> print ;','statement',2,'p_statement','Parser.py',64),
  ('statement -> continue ;','statement',2,'p_statement','Parser.py',65),
  ('statement -> break ;','statement',2,'p_statement','Parser.py',66),
  ('statement -> return ;','statement',2,'p_statement','Parser.py',67),
  ('statement -> if','statement',1,'p_statement','Parser.py',68),
  ('statement -> for','statement',1,'p_statement','Parser.py',69),
  ('statement -> while','statement',1,'p_statement','Parser.py',70),
  ('statement -> nested_statements','statement',1,'p_statement','Parser.py',71),
  ('for -> FOR ID ASSIGN expression : expression nested','for',7,'p_for','Parser.py',78),
  ('while -> WHILE condition nested','while',3,'p_while','Parser.py',85),
  ('break -> BREAK','break',1,'p_break','Parser.py',92),
  ('return -> RETURN expression','return',2,'p_return','Parser.py',99),
  ('continue -> CONTINUE','continue',1,'p_continue','Parser.py',106),
  ('print -> PRINT coma_separated','print',2,'p_print','Parser.py',113),
  ('coma_separated -> coma_separated , expression','coma_separated',3,'p_coma_separated','Parser.py',120),
  ('coma_separated -> expression','coma_separated',1,'p_coma_separated_single','Parser.py',128),
  ('assignment -> ID assign_symbol expression','assignment',3,'p_assignment','Parser.py',135),
  ('assignment -> ID slice assign_symbol expression','assignment',4,'p_slice_assignment','Parser.py',142),
  ('assign_symbol -> ASSIGN','assign_symbol',1,'p_assign','Parser.py',149),
  ('assign_symbol -> SUBASSIGN','assign_symbol',1,'p_assign','Parser.py',150),
  ('assign_symbol -> ADDASSIGN','assign_symbol',1,'p_assign','Parser.py',151),
  ('assign_symbol -> DIVASSIGN','assign_symbol',1,'p_assign','Parser.py',152),
  ('assign_symbol -> MULTASSIGN','assign_symbol',1,'p_assign','Parser.py',153),
  ('expression -> built_in_function ( expression_list )','expression',4,'p_expression_function_call','Parser.py',160),
  ('expression_list -> expression_list , expression','expression_list',3,'p_expression_list','Parser.py',167),
  ('expression_list -> expression','expression_list',1,'p_expression_list_single','Parser.py',174),
  ('expression -> term','expression',1,'p_expression_term','Parser.py',181),
  ('expression -> expression + term','expression',3,'p_expression_binary_ops','Parser.py',188),
  ('expression -> expression - term','expression',3,'p_expression_binary_ops','Parser.py',189),
  ('expression -> expression / term','expression',3,'p_expression_binary_ops','Parser.py',190),
  ('expression -> expression * term','expression',3,'p_expression_binary_ops','Parser.py',191),
  ('expression -> expression EQL term','expression',3,'p_expression_relational_ops','Parser.py',198),
  ('expression -> expression NEQ term','expression',3,'p_expression_relational_ops','Parser.py',199),
  ('expression -> expression GT term','expression',3,'p_expression_relational_ops','Parser.py',200),
  ('expression -> expression GTE term','expression',3,'p_expression_relational_ops','Parser.py',201),
  ('expression -> expression LT term','expression',3,'p_expression_relational_ops','Parser.py',202),
  ('expression -> expression LTE term','expression',3,'p_expression_relational_ops','Parser.py',203),
  ('expression -> - term','expression',2,'p_expression_unary','Parser.py',210),
  ('expression -> expression TRANSPOSE','expression',2,'p_vector_transpose','Parser.py',217),
  ('expression -> ID dot_operation term','expression',3,'p_expression_id_func_call','Parser.py',224),
  ('expression -> vector dot_operation term','expression',3,'p_expression_vector_func_call','Parser.py',232),
  ('dot_operation -> DOTADD','dot_operation',1,'p_dot_operation','Parser.py',239),
  ('dot_operation -> DOTSUB','dot_operation',1,'p_dot_operation','Parser.py',240),
  ('dot_operation -> DOTMUL','dot_operation',1,'p_dot_operation','Parser.py',241),
  ('dot_operation -> DOTDIV','dot_operation',1,'p_dot_operation','Parser.py',242),
  ('vector -> [ vector_contents ]','vector',3,'p_vector','Parser.py',249),
  ('vector -> [ ]','vector',2,'p_vector_empty','Parser.py',256),
  ('vector_contents -> vector_contents , vector_element','vector_contents',3,'p_vector_contents_list','Parser.py',263),
  ('vector_contents -> vector_element','vector_contents',1,'p_vector_contents_single','Parser.py',271),
  ('vector_element -> term','vector_element',1,'p_vector_element','Parser.py',278),
  ('slice -> [ slice_contents ]','slice',3,'p_slice','Parser.py',285),
  ('slice_contents -> slice_contents , range','slice_contents',3,'p_slice_contents','Parser.py',292),
  ('slice_contents -> range','slice_contents',1,'p_slice_contents_single','Parser.py',300),
  ('range -> expression : expression','range',3,'p_range','Parser.py',307),
  ('range -> expression :','range',2,'p_range_startless','Parser.py',314),
  ('range -> : expression','range',2,'p_range_endless','Parser.py',321),
  ('range -> expression','range',1,'p_range_simple','Parser.py',328),
  ('if -> IF condition nested','if',3,'p_if','Parser.py',335),
  ('if -> IF condition nested ELSE nested','if',5,'p_if_else','Parser.py',342),
  ('condition -> ( expression )','condition',3,'p_condition','Parser.py',349),
  ('nested -> statement','nested',1,'p_nested','Parser.py',356),
  ('nested_statements -> nested_empty','nested_statements',1,'p_nested_statements','Parser.py',364),
  ('nested_statements -> nested_statements_list','nested_statements',1,'p_nested_statements','Parser.py',365),
  ('nested_statements_list -> { statements_list }','nested_statements_list',3,'p_nested_statements_list','Parser.py',372),
  ('nested_empty -> { }','nested_empty',2,'p_nested_statements_empty','Parser.py',379),
  ('term -> ( expression )','term',3,'p_term','Parser.py',386),
  ('term -> vector','term',1,'p_term_vector','Parser.py',393),
  ('term -> INTNUM','term',1,'p_term_primitive_int','Parser.py',400),
  ('term -> FLOATNUM','term',1,'p_term_primitive_float','Parser.py',407),
  ('term -> STR','term',1,'p_term_primitive_str','Parser.py',414),
  ('term -> ID','term',1,'p_term_id','Parser.py',421),
  ('built_in_function -> EYE','built_in_function',1,'p_built_in_function','Parser.py',428),
  ('built_in_function -> ONES','built_in_function',1,'p_built_in_function','Parser.py',429),
  ('built_in_function -> ZEROS','built_in_function',1,'p_built_in_function','Parser.py',430),
]
