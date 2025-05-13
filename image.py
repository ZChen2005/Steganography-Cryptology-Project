from PIL import Image

def imageEncoder(inputImagePath, outputImagePath, secretMessage):
    # Setting up the image
    image = Image.open(inputImagePath)
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Making a copy of the image
    encodedImage = image.copy()
    width, height = image.size

    # Turning the message into its 8-bit binary form (array) + add a delimiter to know when the message ends
    # Using 1010110110 because I don't think anyone will use ¶ in a message or at least I hope not
    binaryMessage = ''.join(format(ord(c), '08b') for c in secretMessage) + '10110110'

    # placing the message in the image by going through the pixels row by row
    index = 0
    for row in range(height):
        for col in range(width):
            pixel = list(image.getpixel((col, row)))
            for n in range(3):  # iterating through R, G, B
                if index < len(binaryMessage):
                    # replacing the least significant bit with the bit from the message
                    pixel[n] = pixel[n] & ~1 | int(binaryMessage[index])
                    index += 1
            # updates the pixel with the modified color
            encodedImage.putpixel((col, row), tuple(pixel))
            if index >= len(binaryMessage):
                break
        if index >= len(binaryMessage):
            break

    encodedImage.save(outputImagePath)


def imageDecoder(image_path):
    image = Image.open(image_path)
    if image.mode != "RGB":
        image = image.convert("RGB")

    width, height = image.size

    # setting up the message to add on to later
    binaryMessage = ''

    # extracting LSB from all the pixels
    for row in range(height):
        for col in range(width):
            pixel = image.getpixel((col, row))
            for n in range(3):  # iterating through R, G, B
                binaryMessage += str(pixel[n] & 1)

    # Splitting binaryMessage by 8 bits (bytes)
    bytesList = [binaryMessage[i:i + 8] for i in range(0, len(binaryMessage), 8)]

    # empty string to store the translated message
    decodedMessage = ''

    # going through all the bytes and translating them
    for byte in bytesList:
        # checking for the byte that signals the end of the message
        if byte == '10110110':
            break
        decodedMessage += chr(int(byte, 2))
    print(decodedMessage)

longMsg = ''
i = 100000
msg = "Good Luck With Finals!! "
#for j in range(0, i):
#    longMsg += msg

inputImagePath = "E:/College Coding/Steganography-Cryptology-Project/image/.venv/bird.png"
outputImagePath = "E:/College Coding/Steganography-Cryptology-Project/image/.venv/testing.png"
imageEncoder(inputImagePath, outputImagePath, longMsg)
imageDecoder(outputImagePath)
