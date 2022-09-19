from PIL import Image

answers = "1) My full name is William David Echols but I go by Will Echols. 2) Currently, I’m a freshman general engineering student, but I hope to ETAM into Computer Science. 9) Spending time with friends and family, working on a personal project (especially with programming), trying new things, learning different perspectives 16) Learning about real world problems, aspirations for a better future, seeing other people succeed 17) My passion is to develop myself and the people around me into the best versions of ourselves in order to make a difference 24) I used enterprise server computers to compute the most accurate calculation of the natural log of 2 to date"

def chars_in_a_row(char, string):
    in_a_row = []
    current = 0
    for i in range(len(string)):
        if string[i] == char:
            current += 1
        else:
            if current != 0:
                in_a_row.append(current)
            current = 0
    return in_a_row

def main():
    current_char = 0

    image = Image.open("image2.png")
    image = image.resize((100, 100))
    
    scale = ".,-^'|!*%&#"

    chars = []
    (width, height) = image.size
    for y in range(0, height - 1):
        line = ""
        for x in range(0, width - 1):

            (r, g, b, a) = image.getpixel((x, y))
            pixel_brightness = r + g + b
            selector = int((pixel_brightness / 255 / 3) * (len(scale) - 1))

            if 6 <= selector <= 9 and y >= 30 and 20 <= x <= 60 and current_char < len(answers):
                line += answers[current_char]
                current_char += 1
            else:
                line += scale[selector]

        chars.append(line)

    with open("image.txt", "w") as file:
        for line in chars:
            file.write(line)
            file.write("\n")
        file.close()


main()