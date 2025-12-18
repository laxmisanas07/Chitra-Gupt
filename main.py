import cv2
import numpy as np
import os

# ==========================================
# 🕵️‍♂️ CHITRA-GUPT: THE STEGANOGRAPHY TOOL
# ==========================================

def msg_to_bin(msg):
    if type(msg) == str:
        return ''.join([format(ord(i), "08b") for i in msg])
    elif type(msg) == bytes or type(msg) == np.ndarray:
        return [format(i, "08b") for i in msg]
    elif type(msg) == int or type(msg) == np.uint8:
        return format(msg, "08b")
    else:
        raise TypeError("Input type not supported")

def hide_data(img, data):
    # Secret key taaki pata chale message kahan khatam hua
    data += "#####" 
    
    data_index = 0
    binary_data = msg_to_bin(data)
    data_len = len(binary_data)
    
    # Image copy karte hain taaki original kharab na ho
    encoded_img = img.copy()
    
    # Har pixel mein data chupana (LSB Algorithm)
    for values in encoded_img:
        for pixel in values:
            # R, G, B channels
            for n in range(0, 3):
                if data_index < data_len:
                    # Last bit replace kar rahe hain
                    pixel[n] = int(bin(pixel[n])[2:9] + binary_data[data_index], 2)
                    data_index += 1
                if data_index >= data_len:
                    break
    return encoded_img

def show_data(img):
    binary_data = ""
    for values in img:
        for pixel in values:
            for n in range(0, 3):
                binary_data += (bin(pixel[n])[2:][-1])

    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
    
    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        if decoded_data[-5:] == "#####": # Secret key mil gayi
            return decoded_data[:-5]
    return "❌ Koi Secret Message nahi mila is photo mein."

# ==========================================
# USER INTERFACE
# ==========================================
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\n🕵️‍♂️ --- CHITRA-GUPT: IMAGE STEGANOGRAPHY --- 🕵️‍♂️")
    print("1. Encode (Photo mein message chupana hai)")
    print("2. Decode (Photo se message padhna hai)")
    
    choice = input("\n👉 Option number likh (1 ya 2): ")

    if choice == '1':
        img_name = input("🖼️  Original Image ka naam (e.g. input.png): ")
        if not os.path.exists(img_name):
            print("❌ Error: File nahi mili! Folder check kar.")
            return
            
        image = cv2.imread(img_name)
        data = input("💬 Secret Message likh: ")
        
        print("⏳ Encoding chal rahi hai...")
        encoded_img = hide_data(image, data)
        
        output_name = "secret_image.png"
        cv2.imwrite(output_name, encoded_img)
        print(f"\n✅ SUCCESS! Secret image save ho gayi: {output_name}")
        print("🤫 Ab ye photo apne dost ko bhej de.")

    elif choice == '2':
        img_name = input("🖼️  Secret Image ka naam (e.g. secret_image.png): ")
        if not os.path.exists(img_name):
            print("❌ Error: File nahi mili!")
            return

        print("⏳ Decoding chal rahi hai...")
        image = cv2.imread(img_name)
        
        text = show_data(image)
        print(f"\n🔓 KHUFIYA SANDESH:\n{'-'*30}\n{text}\n{'-'*30}")

    else:
        print("❌ Galat option bhai. Phir se try kar.")

if __name__ == "__main__":
    main()