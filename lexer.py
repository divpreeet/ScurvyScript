from tokens import Doubloon, Piece8, Operation, Declaration, Booty, Boolean, Comparison, Reserved

# hoist ye_flag = 50

class Lexer:
    # while <expr> do <statement>
    digits = "0123456789"
    letters = "abcdefghijklmnopqrstuvwxyz"
    operations = "+-/*()="
    stopwords = [" "]
    declarations = ["hoist"]
    boolean = ["and", "or", "not"]
    comparisons = [">", "<", ">=", "<=", "?="]
    specialCharacters = "><=?"
    reserved = ["if", "elif", "else", "do", "while", "parley"]

    def __init__(self, text):
        self.text = text
        self.idx = 0
        self.tokens = []
        self.char = self.text[self.idx]
        self.token = None
    
    def tokenize(self):
        while self.idx < len(self.text):
            if self.char in Lexer.digits:
                self.token = self.extract_number()
            
            elif self.char in Lexer.operations:
                self.token = Operation(self.char)
                self.move()
            
            elif self.char in Lexer.stopwords:
                self.move()
                continue

            elif self.char in Lexer.letters:
                word = self.extract_word()

                if word in Lexer.declarations:
                    self.token = Declaration(word)
                elif word in Lexer.boolean:
                    self.token = Boolean(word)
                elif word in Lexer.reserved:
                    self.token = Reserved(word)
                elif word == "parley":
                    self.token = Reserved(word)
                else:
                    self.token = Booty(word)
            
            elif self.char in Lexer.specialCharacters:
                comparisonOperator = ""
                while self.char in Lexer.specialCharacters and self.idx < len(self.text):
                    comparisonOperator += self.char
                    self.move()
                
                self.token = Comparison(comparisonOperator)
            
            self.tokens.append(self.token)
        
        return self.tokens

    def extract_number(self):
        number = ""
        isFloat = False
        while (self.char in Lexer.digits or self.char == ".") and (self.idx < len(self.text)):
            if self.char == ".":
                isFloat = True
            number += self.char
            self.move()
        
        return Doubloon(number) if not isFloat else Piece8(number)
    
    def extract_word(self):
        word = ""
        while self.char in Lexer.letters and self.idx < len(self.text):
            word += self.char
            self.move()
        
        return word
    
    def move(self):
        self.idx += 1
        if self.idx < len(self.text):
            self.char = self.text[self.idx]

