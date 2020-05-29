import rsa

def getPNGSygnatureAsBytes():
    sygnature = [137, 80, 78, 71, 13, 10, 26, 10]
    return bytearray(sygnature)

def encrypt_chunks(chunksArray, publicKey):
    intToByteSize = 128
    frameSize = 64

    file = open("zaszyfrowane.png", "w+b")
    file.write(getPNGSygnatureAsBytes())

    chunkIterator = 0
    while chunkIterator < len(chunksArray):
        chunk = chunksArray[chunkIterator]
        if(chunk.getChunkTypeText() == 'IDAT'):
            # Encrypt chunk Length
            lengthArray = []
            encryptedLength = rsa.encryptArray(publicKey, frameSize, chunk.lengthArray)
            for lengthFrame in encryptedLength:
                byteEncryptedLength = (lengthFrame).to_bytes(intToByteSize,byteorder='big')
                for byte in byteEncryptedLength:
                    lengthArray.append(byte)

            # Encrypt chunk data
            newDataArray = []
            encryptedData = rsa.encryptArray(publicKey, frameSize, chunk.dataArray)
            for dataFrame in encryptedData:
                byteEncryptedData = (dataFrame).to_bytes(intToByteSize,byteorder='big')
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
    intToByteSize = 128
    frameSize = 64

    file = open("odszyfrowane.png", "w+b")
    file.write(getPNGSygnatureAsBytes())
    
    chunkIterator = 0
    while chunkIterator < len(chunksArray):
        chunk = chunksArray[chunkIterator]
        if(chunk.getChunkTypeText() == 'IDAT'):
            chunkFrames = []

            frames = len(chunk.dataArray) / intToByteSize

            frame = 0
            byte = 0
            while frame < frames:
                frameData = []

                while byte < (intToByteSize * (frame + 1)):
                    frameData.append(chunk.dataArray[byte])
                    byte += 1
                
                encryptedData = int.from_bytes(frameData,byteorder='big')
                chunkFrames.append(encryptedData)
                frame +=1

            decryptedData = rsa.decryptArray(privateKey, frameSize, chunkFrames)

            chunk.lengthArray = decryptedData[0:4]
            chunk.dataArray = decryptedData[4::]
        
        file.write(chunk.getChunkAsList())
        chunkIterator += 1
