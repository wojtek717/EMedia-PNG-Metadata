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
        chunk = chunksArray[chunkIterator]
        if(chunk.getChunkTypeText() == 'IDAT'):
            # Encrypt chunk Length
            lengthArray = []
            encryptedLength = rsa.encryptArray(publicKey, 64, chunk.lengthArray)
            for lengthFrame in encryptedLength:
                byteEncryptedLength = (lengthFrame).to_bytes(32,byteorder='big')
                for byte in byteEncryptedLength:
                    lengthArray.append(byte)

            # Encrypt chunk data
            newDataArray = []
            encryptedData = rsa.encryptArray(publicKey, 64, chunk.dataArray)
            for dataFrame in encryptedData:
                byteEncryptedData = (dataFrame).to_bytes(32,byteorder='big')
                for byte in byteEncryptedData:
                    newDataArray.append(byte)

            # Count new chunk length
            fullDataArray = lengthArray + newDataArray # At front place old chunk length

            newChunkLength = len(fullDataArray)
            newChunkLengthBytes = (newChunkLength).to_bytes(4,byteorder='big')
            newChunkLengthArray = []
            for byte in newChunkLengthBytes:
                newChunkLengthArray.append(byte)

            chunk.lengthArray = newChunkLengthArray
            chunk.dataArray = fullDataArray
        
        file.write(chunk.getChunkAsList())
        chunkIterator += 1

def decrypt_chunks(chunksArray, privateKey):
    
    chunkIterator = 0
    while chunkIterator < len(chunksArray):
        if(chunksArray[chunkIterator].getChunkTypeText() == 'IDAT'):
            rsa.decrypt(privateKey, chunksArray[chunkIterator].dataArray)
        chunkIterator += 1
