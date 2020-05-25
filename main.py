import chunk as PNGChunk
import chunksDecoder as CDecoder
import chunksAnonimizer as CAnonimizer
import fourrier as fr
import signature 
import chunkCrypter
import rsa

def menu():
    keys = rsa.generate_keys(100)
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
            chunkCrypter.encrypt_chunks(fileChunks, keys.publicKey)

        #MENU EXCEPTION
        else:
            print("Wrong option, try again.")
     

    
def main():
    menu()


if __name__ == "__main__":
    main()
