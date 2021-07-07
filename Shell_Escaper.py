from os import read
import requests , sys , re , optparse , subprocess
from bs4 import BeautifulSoup

#Colores:
sRed   , eRed   = "\033[1;31m" , "\033[1;m"
sGreen , eGreen = "\033[1;54m" , "\033[1;m"
sWhite , eWhite = "\033[1;37m" , "\033[1;m"
sGray  , eGray  = "\033[1;90m" , "\033[1;m"

def logo():
    print('''\033[2;31m
                                      010                                       
                                      010                                       
                            000000000 010 000000000                             
                       00000000000000 010 00000000000000                        
                    00000000000000000 010 00000000000000000                     
                 00000000000000       010        0000000000000                  
               00000000000       0    010    0          0000000000                
             00000000          00             00           000000000              
           00000000           000             000            00000000            
          00000000           0000             0000             00000000          
         0000000             0000   1111111   0000              00000000         
       0000000                0000111111111110000                0000000        
       000000                 0011111111111111100                 0000000       
      000000                   11111111111111111                   0000000      
     000000                   1111111111111111111                   000000      
     000000                  111111111111111111111                   000000     
    000000                  11111111111111111111111                  000000     
    000000         0000000011111111111111111111111110000000           00000     
    00000       00000000001111111111111111111111111110000000000       000000    
00000000000000 00000000000111111111111111111111111111100000000000 000000000000000
00000000000000           11111111111111111111111111111            000000000000000
    00000                11111111111111111111111111111                00000    
    000000         00000001111111111111111111111111111000000          00000     
    000000       0000000 11111111111111111111111111111 00000000      000000     
     000000    0000000   11111111111111111111111111111   0000000     00000    
     000000    00         111111111111111111111111111         00    000000      
      000000            00001111111111111111111111100000           000000       
       0000000        00000001111111111111111111110000000         0000000       
        0000000      000000  111111111111111111111   000000     00000000        
         0000000    000        11111111111111111        000    0000000          
          00000000                 111111111                 00000000           
            000000000                                      000000000            
             0000000000                                 000000000              
                00000000000           010           000000000000                
                  000000000000000     010     000000000000000                   
                     0000000000000000 010 0000000000000000                      
                         000000000000 010 0000000000000                         
                              0000000 010 0000000                               
                                      010                                       
                                      010                                      

                   -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
                   +      ..| Shell_Escaper v1.0 |..      +
                   -                                      -
                   -              By: Mesh3l              -
                   +         Twitter: Mesh3l_911          +
                   -+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+                                                 
\033[1;m''')

splittedUid  = []
splittedSudo = []

def Args():
    Parser = optparse.OptionParser()
    Parser.add_option("--upath", "--upath", dest="uidPath", help="Path of the file that has the binaries with setuid bit")
    Parser.add_option("--spath", "--spath", dest="soduPath", help="Path of the Sudo file")
    Parser.add_option("--user", "--user", dest="Username", help="Ssh Username")
    Parser.add_option("--pass", "--pass", dest="Password", help="Ssh Password")
    Parser.add_option("--host", "--host", dest="Host", help="Ssh Host")
    Parser.add_option("--port", "--port", dest="Port", help="Ssh Port")
    Parser.add_option("--key", "--key", dest="PrivateKey", help="Path of the ssh PrivateKey")
    (arguments, values) = Parser.parse_args()

    return arguments


currentPath = subprocess.run(["pwd", ""], capture_output=True,shell=True).stdout.decode().rstrip('\n')
sPath = currentPath+"/sudo.txt"
uPath = currentPath+"/uid.txt"

#A function to send a remote command via ssh ( Username,PrivateKey,Host,Port )
def sshK(PrivateKey,Username,Host,Port):

    uidCommand  = subprocess.run(["ssh -i "+PrivateKey+" " +Username+"@"+Host+" -p "+Port+" 'find / -type f -a \( -perm -u+s \) -exec ls  {} \; 2> /dev/null' ", ""], capture_output=True,shell=True).stdout.decode()
    soduCommand  = subprocess.run(["ssh -i "+PrivateKey+" " +Username+"@"+Host+" -p "+Port+" 'sudo -l' ", ""], capture_output=True,shell=True).stdout.decode()

    with open(uPath, 'w') as Uid , open(sPath, 'w') as Sudo:
        Uid.write(str(uidCommand))
        Sudo.write(str(soduCommand))
        Uid.close()
        Sudo.close()

    with open(uPath, 'r') as Uid , open(sPath, 'r') as Sudo:

        for _ in Uid.read().splitlines():
            if '/' in _:
                Splitted = _.rsplit('/',1)[-1]
                splittedUid.append(Splitted)
            Splitted = _.rsplit('/',1)[-1]
            splittedUid.append(Splitted)
        print("\n")

        for _ in Sudo.read().splitlines():
            if '/' in _:
                Splitted = _.rsplit('/',1)[-1]
                splittedSudo.append(Splitted)
        print("\n")

#A function to send a remote command via sshpass ( Username,Password,Host,Port ) ( Not Recommended for real life engagements )
def sshPass(Password,Port,Username,Host):

    uidCommand  = subprocess.run(["sshpass -p "+Password+" ssh -p "+Port+" -o StrictHostKeyChecking=no "+Username+"@"+Host+" 'find / -type f -a \( -perm -u+s \) -exec ls  {} \; 2> /dev/null'", ""], capture_output=True,shell=True).stdout.decode()
    soduCommand = subprocess.run(["sshpass -p "+Password+" ssh -p "+Port+" -o StrictHostKeyChecking=no "+Username+"@"+Host+" 'sudo -l'", ""], capture_output=True,shell=True).stdout.decode()
    
    with open(uPath, 'w') as Uid , open(sPath, 'w') as Sudo:
        Uid.write(str(uidCommand))
        Sudo.write(str(soduCommand))
        Uid.close()
        Sudo.close()

    with open(uPath, 'r') as Uid , open(sPath, 'r') as Sudo:
        
        for _ in Uid.read().splitlines():
            if '/' in _:
                Splitted = _.rsplit('/',1)[-1]
                splittedUid.append(Splitted)
        print("\n")

        for _ in Sudo.read().splitlines():
            if '/' in _:
                Splitted = _.rsplit('/',1)[-1]
                splittedSudo.append(Splitted)
        print("\n")

#A function to append the non-absolute path Binaries with setuid bit from a file 
def appendUid(uidPath):

    with open(uidPath, 'r') as results:
        for _ in results.read().splitlines():
            if '/' in _:
                Splitted = _.rsplit('/',1)[-1]
                splittedUid.append(Splitted)
        print("\n")

#A function to append the non-absolute path Binaries with setuid bit from a file to a list
def appendSudo(soduPath):

    with open(soduPath, 'r') as results:
        for _ in results.read().splitlines():
            if '/' in _:
                Splitted = _.rsplit('/',1)[-1]
                splittedSudo.append(Splitted)
        print("\n")

Session = requests.session()
#A function to Scrap the expl0it commands out of GTFOBins by using Regular expression + BeautifulSoup
def uidSudoscraper():

    with open(uPath, 'r') as Uid , open(sPath, 'r') as Sudo:

        print(sGray+"...........|| absolute path Binaries with setuid bit ||..........."+eGray+"")
        for _ in Uid.read().splitlines():
            print(sWhite+_+eWhite)
        print()
        empty = True

        for _ in splittedUid:
            Url = 'https://gtfobins.github.io/gtfobins/'
            Search = Session.get(Url+_).text

            if "Page not found" not in Search and ">SUID<" in Search :
                regex = re.search(r"<h2 id=\"suid\" class=\"function-name\">SUID</h2>([\s\S]*?)</ul>", Search).group(1)
                Soup = BeautifulSoup(regex, 'html.parser')
                regex2 = re.search(r"<code>([\s\S]*?)</code>",str(Soup)).group(1)
                print("\n"+sWhite+"["+eWhite+""+sGreen+"*"+eGreen+""+sWhite+"] Expl0itaion Found for"+eWhite+" \033[1;54m{}\033[1;m\n".format(_)+"\n"+sGray+regex2+eGray+"\n")
            else:
                print(""+sWhite+"["+eWhite+""+sRed+"!"+eRed+""+sWhite+"] There is no expl0itation for"+eWhite+" \033[1;31m{}\033[1;m".format(_))

        
        print("\n"+sGray+"................|| Sudo ||................"+eGray+"")
        if Sudo.read(1):
            for _ in Sudo.read().splitlines():
                print(sWhite+_+eWhite)
        else:
            print(""+sWhite+"["+eWhite+""+sRed+"!"+eRed+""+sWhite+"] Couldn't be listed ( Permissions could be a reason )")
        print()

        for _ in splittedSudo:
            Url = 'https://gtfobins.github.io/gtfobins/'
            Search = Session.get(Url+_).text


            if "Page not found" not in Search and ">Sudo<" in Search :
                regex = re.search(r"<h2 id=\"sudo\" class=\"function-name\">Sudo</h2>([\s\S]*?)</ul>", Search).group(1)
                Soup = BeautifulSoup(regex, 'html.parser')
                regex2 = re.search(r"<code>([\s\S]*?)</code>",str(Soup)).group(1)
                print("\n"+sWhite+"["+eWhite+""+sGreen+"*"+eGreen+""+sWhite+"] Expl0itaion Found for"+eWhite+" \033[1;54m{}\033[1;m\n".format(_)+"\n"+sGray+regex2+eGray+"\n")
            else:
                print(""+sWhite+"["+eWhite+""+sRed+"!"+eRed+""+sWhite+"] There is no expl0itation for"+eWhite+" \033[1;31m{}\033[1;m".format(_))


def uidScarper(Path):

    with open(Path, 'r') as Uid:
        print(sGray+"...........|| absolute path Binaries with setuid bit ||..........."+eGray+"")
        for _ in Uid.read().splitlines():
            print(sWhite+_+eWhite)
        print()

        for _ in splittedUid:
            Url = 'https://gtfobins.github.io/gtfobins/'
            Search = Session.get(Url+_).text

            if "Page not found" not in Search and ">SUID<" in Search :
                regex = re.search(r"<h2 id=\"suid\" class=\"function-name\">SUID</h2>([\s\S]*?)</ul>", Search).group(1)
                Soup = BeautifulSoup(regex, 'html.parser')
                regex2 = re.search(r"<code>([\s\S]*?)</code>",str(Soup)).group(1)
                print("\n"+sWhite+"["+eWhite+""+sGreen+"*"+eGreen+""+sWhite+"] Expl0itaion Found for"+eWhite+" \033[1;54m{}\033[1;m\n".format(_)+"\n"+sGray+regex2+eGray+"\n")
            else:
                print(""+sWhite+"["+eWhite+""+sRed+"!"+eRed+""+sWhite+"] There is no expl0itation for"+eWhite+" \033[1;31m{}\033[1;m".format(_))


def sudoScrapper(Path):

    with open(Path, 'r') as Sudo:
        print("\n"+sGray+"................|| Sudo ||................"+eGray+"")
        for _ in Sudo.read().splitlines():
            print(sWhite+_+eWhite)
        print()

        for _ in splittedSudo:
            Url = 'https://gtfobins.github.io/gtfobins/'
            Search = Session.get(Url+_).text

            if "Page not found" not in Search and ">Sudo<" in Search :
                regex = re.search(r"<h2 id=\"sudo\" class=\"function-name\">Sudo</h2>([\s\S]*?)</ul>", Search).group(1)
                Soup = BeautifulSoup(regex, 'html.parser')
                regex2 = re.search(r"<code>([\s\S]*?)</code>",str(Soup)).group(1)
                print("\n"+sWhite+"["+eWhite+""+sGreen+"*"+eGreen+""+sWhite+"] Expl0itaion Found for"+eWhite+" \033[1;54m{}\033[1;m\n".format(_)+"\n"+sGray+regex2+eGray+"\n")
            else:
                print(""+sWhite+"["+eWhite+""+sRed+"!"+eRed+""+sWhite+"] There is no expl0itation for"+eWhite+" \033[1;31m{}\033[1;m".format(_))

        
        
def main():
    arguments = Args()
    if len(sys.argv) == 3 and '--upath' in str(sys.argv):
        logo()
        appendUid(arguments.uidPath)
        uidScarper(arguments.uidPath)
        print()
    elif len(sys.argv) == 3 and '--spath' in str(sys.argv):
        logo()
        appendSudo(arguments.soduPath)
        sudoScrapper(arguments.soduPath)
        print()
    elif len(sys.argv) == 9 and '--key' in str(sys.argv):
        logo()
        sshK(arguments.PrivateKey, arguments.Username, arguments.Host, arguments.Port)
        uidSudoscraper()
        print()
    elif len(sys.argv) == 9 and '--pass' in str(sys.argv):
        logo()
        sshPass(arguments.Password, arguments.Port, arguments.Username, arguments.Host)
        uidSudoscraper()
        print()

    else:
        logo()
        print ("\n\033[2;31mUsage:\033[1;m\n\n"+sWhite+"python3 Shell_Escaper.py --user <SSh_Username> --key <SShPrivateKey_Path> --port <SSh_Port> --host <SSh_Host>"+eWhite+"\n\n\033[2;31mor\033[1;m\n\n"+sWhite+"python3 Shell_Escaper.py --user <SSh_Username> --pass <SSh_Password> --port <SSh_Port> --host <SSh_Host>"+eWhite+"\n\n\033[2;31mor\033[1;m\n\n"+sWhite+"python3 Shell_Escaper.py --upath <UID_Path>"+eWhite+"\n\n\033[2;31mor\033[1;m\n\n"+sWhite+"python3 Shell_Escaper.py --spath <Sudo_Path>"+eWhite+"\n\n\033[2;31mfor further information \033[1;m\n\n"+sWhite+"python3 Shell_Escaper.py --help"+eWhite+"\n")
    quit()

  
if __name__ == '__main__':
    main()





