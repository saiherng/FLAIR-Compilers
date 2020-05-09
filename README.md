# Flair_compiler
Team : Sai, Rishabh, Phu  
Team Name : WillCode4Food

Known bugs: What's a bug!

To run the type checker, run flairc or src/mainCodeGenerator

Features: 
 Attempted extra credit. 
 Documentation in main folder
 	
;; ------------------------------------
               Archived
;; ------------------------------------


Scanner functions:
    1) next()  => get next token
    2) peek()  => see next token


;; -------------------------------------
;; unambiguous_grammar.txt
;;--------------------------------------

This text file has unambigous grammar which has productions like:

	1) <NONEMPTYFORMALS> ::= <FORMAL> <NONEMPTY-F-REST>

        2) <NONEMPTY-F-REST> ::= , <FORMAL> <NONEMPTY-F-REST>
                               | e

	which leads to cycle of two and multi-level while finding the follow of productions.

;;-------------------------------------
;; unambiguous_grammar2.txt
;;-------------------------------------

After refactoring further the above productions to:
	
	1) <NONEMPTYFORMALS> ::= <FORMAL> <NONEMPTY-F-REST>

        2) <NONEMPTY-F-REST> ::= , <FORMAL> <NONEMPTY-F-REST>
                               | e

	This removes the cycle of two productions while finding the "follow", but it still cannot
	remove multi-level cycles.

;;-------------------------------------
;; first_follow.txt
;;-------------------------------------

First and follow caculations from unambiguous_grammar.txt

;;--------------------------------------
;; first_follow2.txt
;;--------------------------------------

First and follow caculations from unambiguous_grammar2.txt

=> Although both grammars lead to same set of first and follow's. 

;;---------------------------------------
;; getTerminal.py (in Misc)
;; --------------------------------------

This program takes the first_follow.txt file and returns the list of terminals from "first" of all productions.
It helped in creating the parsing table.

;;---------------------------------------
;; flr_parser.py (in Misc)
;; --------------------------------------

Program trying to create the parse table with key as a tuple of objects. The instances of class Terminals's __hash__() was 
failing at some edge cases, so it was given up on. Instead I chose to go more hard coded way and created the main parser.py 
(although I was very sad!) (made it work and shifted to src)

;;---------------------------------------
;; parser_complete_enum.py (in Misc)
;; --------------------------------------

Program trying to create the parse table with key as a tuple of enums. It involved creating an enum class for tokens that the scanner
passed, which was redundant and time consuming. I started it when I was frustrated with the __hash__() functions of the Tokens which 
fails at cases like <BOOLEAN>, <NUMBER>, <IDENTIFIER>. Since, these do not have any self.value while creating parse table, their hash
function had to be modified.

;;---------------------------------------
;; parser_enum_obj.py (in src)
;; --------------------------------------

Program trying to create the parse table with key as a tuple of NonTerminal (enums) and Token object. This is a middle ground between
above two parsers. It involved hard coding the NonTerminal class, which is actually sad and I am trying to improve it, but as they say
if your program works, don't touch it. So, I am delaying that idea for the time being. The hash  function is modified to suit the needs.
(working but shifted to misc since we have complete object implementation of the parse dict)

;; ---------------------------
;; parsing_table.txt
;; ---------------------------

Correct version of parsing table, but contains two entries for few columns.

;; ---------------------------
;; partable2.txt
;; ---------------------------

Slightly incorrect version, but runs parser perfectly. I still do not understand why is it running parser.


=========================================================================================================
--------------------------NEWLY ADDED SINCE LAST TIME ---------------------------------------------------
=========================================================================================================

--------------
/doc/f.py
-------------
Script to convert the text parse table into python dictionary.

--------------
/doc/pythagoras.flr
-------------
A program in flair to decide whether the three input sides (hypotenuse, perpendicular, adjacent) is a right triangle.

--------------
/doc/grammar_with_SA.txt
-------------
Grammar with semantic actions

--------------
/src/flr_ast
-------------
Classes to implement the semnatic actions

--------------
/doc/AST-Classes-and-Records.txt
-------------
Initials planned classes to implement the semantic action


------------------------------------------------------
Some other info
------------------------------------------------------

We changed out scanner. We created individual tokens for each keyword and arithmetic operator.
We changed out scanner. We hard coded(the program did) the parse table.
