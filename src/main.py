"""
    @author         :  Phu Vijaranakorn, Sai Herng, Rishabh Dalal
    @description    :  Scanner for language Flair
    @since          :  12 Sept. 2018
 
"""

from scanner2 import Scanner 
from flr_token import Token, TokenType

def main():
    token = Token(TokenType.EOF)
    
    file = open("program.flr", 'r')
    program = file.read()
    scanner = Scanner(program)

    print("Tokens:\n")
    while True:
        tkn = scanner.get_next_token()
        if not tkn:
            print("Something is wrong. Correct me.")
            break
        if tkn.isEOF():                  ##Not working
            print("\nExecution complete.")
            break 
        print(tkn)

if __name__ == "__main__":
    main()
    
