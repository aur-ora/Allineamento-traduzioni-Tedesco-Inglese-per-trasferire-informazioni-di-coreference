import MyWork
# Defining main function
def main():
    enTXT = open("junger.marbledue.en.txt", "r")
    deTXT = open("junger.marmordue.de.txt", "r")
    fifth = open("sentences.txt", "r")
    funf = open("sätze.txt", "r")
    en = open("one.txt", "r")
    de = open("ein.txt", "r")
    #print((MyWork.createSet_en(englischTXT)))
    #print((MyWork.createSet_de(deutschTXT)))
    print(MyWork.alignmentBabelNet.sameSentence(enTXT, deTXT))
    #print(MyWork.getCoreference("conrad.darkness.en.txt"))

if __name__ == "__main__":
      main()