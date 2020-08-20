import MyWork
# Defining main function
def main():
    englishTXT = open("provaEN.txt", "r")
    germanTXT = open("provaDE.txt", "r")
    return (MyWork.createSet_en(englishTXT))
    return (MyWork.createSet_de(germanTXT))

if __name__ == "__main__":
      main()