import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def main():
    print("Hello")
    img=mpimg.imread('exampleImage.png')
    imgplot = plt.imshow(img)
    plt.show()


if __name__ == "__main__":
    main()
