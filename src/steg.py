from PIL import Image
import os

# Convert text to binary
def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

# Convert binary to text
def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)

# Hide text in image (same directory output)
def hide_text(image_path, secret_text):
    image = Image.open(image_path)
    pixels = image.load()

    binary_text = text_to_binary(secret_text) + "1111111111111110"
    data_index = 0

    for y in range(image.height):
        for x in range(image.width):
            if data_index < len(binary_text):
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(binary_text[data_index])
                pixels[x, y] = (r, g, b)
                data_index += 1

    # Create output path in same directory
    directory, filename = os.path.split(image_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(directory, f"{name}_stego{ext}")

    image.save(output_path)
    print(f"[+] Text hidden successfully in {output_path}")

# Extract text from image
def extract_text(image_path):
    image = Image.open(image_path)
    pixels = image.load()

    binary_data = ""

    for y in range(image.height):
        for x in range(image.width):
            r, g, b = pixels[x, y]
            binary_data += str(r & 1)

            if binary_data.endswith("1111111111111110"):
                binary_data = binary_data[:-16]
                secret_text = binary_to_text(binary_data)
                print("[+] Hidden text extracted:")
                print(secret_text)
                return

    print("[-] No hidden text found")

# CLI
if __name__ == "__main__":
    print("1. Hide Text in Image")
    print("2. Extract Text from Image")
    choice = input("Choose option: ")

    if choice == "1":
        img = input("Image path: ")
        text = input("Text to hide: ")
        hide_text(img, text)

    elif choice == "2":
        img = input("Image path: ")
        extract_text(img)

    else:
        print("Invalid option")
