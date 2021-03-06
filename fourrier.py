from PIL import Image, ImageFile
import numpy as np
import matplotlib.pyplot as plt


def showFourrierSpectrum(filePath, fileName):
    plt.figure(figsize=(6.4*4, 4.8*4), constrained_layout=False)

    im = Image.open(filePath)
    img_c = im.convert('L')
    img_c1 = np.array(img_c)

    img_c2 = np.fft.fft2(img_c1)
    img_c3 = np.fft.fftshift(img_c2)
    img_c4 = np.fft.ifft2(img_c2)

    plt.subplot(221), plt.imshow(img_c1, "gray"), plt.title("Image")
    plt.subplot(222), plt.imshow(20*np.log(1+np.abs(img_c2)), "gray"), plt.title("Spectrum")
    plt.subplot(223), plt.imshow(20*np.log(1+np.abs(img_c3)), "gray"), plt.title("Centered")
    plt.subplot(224), plt.imshow(np.angle(img_c4), "gray"), plt.title("Phase angle")

    plt.savefig("figures/" + fileName)
    plt.show()


def showImage(filename):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    im = Image.open(filename)
    im.show()