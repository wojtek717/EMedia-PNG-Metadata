from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def showFourrierSpectrum(filename):
    plt.figure(figsize=(6.4*4, 4.8*4), constrained_layout=False)

    im = Image.open(filename)
    img_c1 = np.array(im)

    img_c2 = np.fft.fft2(img_c1)
    img_c3 = np.fft.fftshift(img_c2)
    img_c4 = np.fft.ifft2(img_c2)

    plt.subplot(221), plt.imshow(img_c1, "gray"), plt.title("Original Image")
    plt.subplot(222), plt.imshow(20*np.log(1+np.abs(img_c2)), "gray"), plt.title("Spectrum")
    plt.subplot(223), plt.imshow(20*np.log(1+np.abs(img_c3)), "gray"), plt.title("Centered")
    plt.subplot(224), plt.imshow(np.abs(img_c4), "gray"), plt.title("Processed Image")

    plt.savefig("figures/mygraph.png")
    plt.show()


def showImage(filename):
     im = Image.open(filename)
     im.show()