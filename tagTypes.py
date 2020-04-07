def getTagTypeString(tagIDNumber):
    if(tagIDNumber == 270):
        return str("ImageDescription")
    elif(tagIDNumber == 315):
        return str("Artist")
    elif(tagIDNumber == 282):
        return str("Image.XResolution")
    elif(tagIDNumber == 283):
        return str("Image.YResolution")
    elif(tagIDNumber == 296):
        return str("Image.ResolutionUnit")
    elif(tagIDNumber == 531):
        return str("Exif.Image.YCbCrPositioning")
    else:
        return str(tagIDNumber)

        

       