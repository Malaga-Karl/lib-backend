class Soundex:
    def __init__(self):
        None
    
    #soundex generator function
    def soundex_generator(self, token):
        #convert the word to upper
        #case for uniformity

        token = token.upper()
        soundex = ""

        #retain the first letter
        soundex += token[0]

        #create dictionariy which maps letters to respective soundex codes
        dictionary = {"BFPV": "1", "CGJKQSXZ" : "2", 
                    "DT": "3", 
                    "L": "4", "MN": "5", "R": "6",
                    "AEIOUHWY":"."}
        
        for char in token[1:]:
            for key in dictionary.keys():
                if char in key:
                    code = dictionary[key]
                    if code != '.':
                        if code != soundex[-1]:
                            soundex += code
        soundex = soundex[:7].ljust(7, "0")

        return soundex