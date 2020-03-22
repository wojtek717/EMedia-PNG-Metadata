import binascii

def main():
    filename = 'ex1.png'
    with open(filename, 'rb') as f:
        content = f.read()
    print(binascii.hexlify(content))


if __name__ == "__main__":
    main()
