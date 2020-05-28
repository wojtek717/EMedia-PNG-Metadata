import chunk as PNGChunk
import chunksDecoder as CDecoder
import chunksAnonimizer as CAnonimizer
import fourrier as fr
import signature 
import chunkCrypter
import rsa

def hardKeys():
    publicKey = rsa.Public_Key(73694415899850154303598464974387916500155653560017898463492565586334598512629668938193677866319577201824782414101422202288978656629001027359659185545904320514137328728814881518794740028462312791288311743345851105571783672934846663649220517815032720260242376756364632394059573393425303956848663358385809589007, 73031160089637948451523977875330906078198376418232611521019794807970232159928675344958706253383880399046128634911325600030539179407241463858781610367217664123656931362645599400775578841871649833781917226946241109459169222567440301255783512154345141852966824954667700324729904054069161465808679747088164064013)
    privateKey = rsa.Private_Key(73694415899850154303598464974387916500155653560017898463492565586334598512629668938193677866319577201824782414101422202288978656629001027359659185545904320514137328728814881518794740028462312791288311743345851105571783672934846663649220517815032720260242376756364632394059573393425303956848663358385809589007, 32116433308255460704311967526307743211715473150184547110434148563659079100663744054717760550454207597508683589788029073062754695111052172703971641821484173807658092407225951934926357158000386658667788679346966297943569232212038349784916285766425235919650557296105576914297712001123951904581797328144373299077)

    return rsa.Keys_Collection(publicKey, privateKey)

def menu():
    #keys = hardKeys() KEEP FOR DEBUG PURPOSE
    keys = rsa.Keys_Collection
    fileinput_FLAG = False

    #attempt to read an image until successfull or user quits
    while(fileinput_FLAG == False):
        file = input("Input the name of a PNG image in /images (Without the extension, type 'quit' to terminate):\n")
        if(file == "quit"):
            print("Program terminated.")
            return 0
        filePath = "images/" + file + ".png"
        fileChunks = []

        # Open and read file into byte array if it exists
        try:
            with open(filePath, 'rb') as f:
                byteArray = f.read()
                
                if(signature.check_sygnature(byteArray) != True):
                    print("Not a PNG file, try again.\n")
                else:
                    print("File read successfully.")
                    fileinput_FLAG = True
                    chunkIndex = 8
                    while chunkIndex != (-1):
                        fileChunks.append(PNGChunk.read_chunk(byteArray, chunkIndex))
                        chunkIndex = fileChunks[-1].nextChunkIndex
        except OSError:
            print("Cant locate \"" + file + "\", try again.\n")


    #MENU PRINT
    fileoperation_FLAG = False
    while(fileoperation_FLAG == False):
        print("\n MENU ====================")
        print("1. View image data.")
        print("2. Show Fourrier' transform.")
        print("3. Anonymize image.")
        print("4. Show image.")
        print("5. Quit.")
        print("6. Encode image.")
        print("7. Decode image.")
        print("8. Generate new RSA keys.")
        print("9. Load RSA keys.")
        try:
            menu_choice = int(input("Choose option: "))
        except:
            menu_choice = 42
        print("")

        #MENU CHOICE 1
        if(menu_choice == 1):
            #show present chunks and what information they hold
            for chunk_it in fileChunks:
                print('Chunk type ->' + chunk_it.getChunkTypeText())
            CDecoder.decode_chunks(fileChunks)
        
        #MENU CHOICE 2
        elif(menu_choice == 2): 
            fr.showFourrierSpectrum(filePath, file)

        #MENU CHOICE 3
        elif(menu_choice == 3): 
            print("Anonymizing image.")
            CAnonimizer.anonimize_chunks(fileChunks, filePath)
            #reload the newly anonymized image
            fileChunks.clear()
            with open(filePath, 'rb') as f:
                byteArray = f.read()
            chunkIndex = 8
            while chunkIndex != (-1):
                fileChunks.append(PNGChunk.read_chunk(byteArray, chunkIndex))
                chunkIndex = fileChunks[-1].nextChunkIndex

        #MENU CHOICE 4
        elif(menu_choice == 4):
            print("Showing image.")
            fr.showImage(filePath)

        #MENU CHOICE 5
        elif(menu_choice == 5):
            print("Program terminated.")
            return 0

        elif(menu_choice == 6):
            print("Encrypting...")
            try:
                chunkCrypter.encrypt_chunks(fileChunks, keys.publicKey)
            except:
                print("LOAD RSA KEYS!")


        elif(menu_choice == 7):
            print("Decrypting...")
            try:
                chunkCrypter.decrypt_chunks(fileChunks, keys.privateKey)
            except:
                print("LOAD RSA KEYS!")

        elif(menu_choice == 8):
            print("Generating new RSA keys...")
            generatedKeys = rsa.generate_keys(512)
            generatedKeys.savePublicKeyToFile("publicKey.txt")
            generatedKeys.savePrivateKeyToFile("privateKey.txt")

        elif(menu_choice == 9):
            print("Loading RSA keys...")
            publicKeyFileName = input("Public Key file: \n")
            privateKeyFileName = input("Private Key file: \n")

            try:
                publicKeyFile = open(publicKeyFileName, "r")
                privateKeyFile = open(privateKeyFileName, "r")
            except:
                print("CAN NOT OPEN FILE")
            else:
                publicKey = rsa.Public_Key(int(publicKeyFile.readline()), int(publicKeyFile.readline()))
                privateKey = rsa.Private_Key(int(privateKeyFile.readline()), int(privateKeyFile.readline()))
                keys = rsa.Keys_Collection(publicKey, privateKey)


        #MENU EXCEPTION
        else:
            print("Wrong option, try again.")
     

    
def main():
    menu()


if __name__ == "__main__":
    main()
