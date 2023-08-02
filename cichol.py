import sys,shutil,os,yaml,subprocess

def sendHelp():
    print("Usage: python3 cichol.py [OPTION]... in=INPUT_DIRECTORY... out=OUTPUT_DIRECTORY... useGameConfig=GAME_ID...\n\nOptions:\n\n   \033[1m-f, --merge-fe3h-data1\033[0m\n       Merge the DATA1.bin file for Fire Emblem: Three Houses.\n       Only use if DATA1.bin is stored in parts, usually because of FAT32 filesize limits. \n       Split using the pattern \"DATA1_part_\" with the GNU coreutils \"split\" command.\n\n   \033[1m--help\033[0m  Display this help and exit.")

if len(sys.argv) < 4:
    sendHelp()
try:
    if sys.argv[1] == "--help":
        sendHelp()
except:
    pass

for arg in sys.argv:
    if arg.lower().startswith("in="):
        dataInDirectory = arg[3,len(arg)]
    if arg.lower().startswith("out="):
        dataOutDirectory = arg[4:len(arg)]
    if arg.lower().startswith("useGameconfig="):
        gameConfig = arg[13:len(arg)]
    if arg.lower() == "-f" or arg == "--merge-fe3h-data1":
        mergeFE3HDATA = True
    else: mergeFE3HDATA1 = False
try: 
    if dataInDirectory is None or dataOutDirectory is None:
        print("Please provide the directory of the new files and the game romfs directory.\nPlease include \"in=\" before the path of the directory containing the new files and \"out=\" before the path of the game's romfs directory. Use \"--help\" for help.")
        sys.exit()
except:
    sys.exit()

if not os.path.isdir(dataInDirectory):
    print("\n" + dataInDirectory + " does not exist\n")
    sys.exit()
if not os.path.isdir(dataOutDirectory):
    print("\n" + dataOutDirectory + " does not exist\n")
    sys.exit()

with open("./gameConfig.yml", 'r') as filesDoc:
    files = yaml.safe_load(filesDoc)

moddedFiles = os.listdir(dataInDirectory)

for gameFile in moddedFiles:
    if gameFile in files[gameConfig]:        
        if mergeFE3HDATA1:
                try:
                    os.remove(dataOutDirectory + files[gameConfig]["DATA1.bin"])
                except:
                    pass
                subprocess.run(["cat", dataInDirectory + "/DATA1_PART_*", ">>", dataOutDirectory + files[gameConfig[gameFile]]])
                subprocess.run("rm", "DATA1_PART_*")
        else:
            gameFilePathOut = (dataOutDirectory + files[gameConfig][gameFile])
            if not os.path.isdir(gameFilePathOut[0:len(gameFilePathOut)-len(gameFile)]):
                subprocess.run("mkdir", "-p", gameFilePathOut[0:len(gameFilePathOut)-len(gameFile)])
            try:
                os.remove(gameFilePathOut)
            except:
                pass
            shutil.copy(dataInDirectory + gameFile, gameFilePathOut)