import MyWork
# Defining main function
def main():
    enTXT = open("junger.marble.en.txt", "r")
    deTXT = open("junger.marmor.de.txt", "r")
    fifth = open("sentences.txt", "r")
    funf = open("sätze.txt", "r")
    en = open("one.txt", "r")
    de = open("ein.txt", "r")
    #print((MyWork.createSet_en(englischTXT)))
    #print((MyWork.createSet_de(deutschTXT)))
    #print(MyWork.alignmentBabelNet.sameSentence(enTXT, deTXT))
    print(MyWork.getCoreference("junger.marble.en.txt"))

if __name__ == "__main__":
      main()