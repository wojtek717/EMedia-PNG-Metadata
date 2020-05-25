import rsa

def getPNGSygnatureAsBytes():
    sygnature = [137, 80, 78, 71, 13, 10, 26, 10]
    return bytearray(sygnature)

def encrypt_chunks(chunksArray, publicKey):

    print("Jestem tutaj")
    file = open("zaszyfrowane.png", "w+b")
    file.write(getPNGSygnatureAsBytes())

    chunkIterator = 0
    while chunkIterator < len(chunksArray):
        if(chunksArray[chunkIterator].getChunkTypeText() == 'IDAT'):
            #print(chunksArray[chunkIterator].dataArray)

        chunkIterator += 1

def decrypt_chunks(chunksArray, privateKey):
    
    chunkIterator = 0
    while chunkIterator < len(chunksArray):
        if(chunksArray[chunkIterator].getChunkTypeText() == 'IDAT'):
            rsa.decrypt(privateKey, chunksArray[chunkIterator].dataArray)
        chunkIterator += 1
