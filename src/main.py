# ./main.sh
# hello world

from textnode import TextNode, TextType

def main():
    text_node = TextNode("This is some text", TextType.LINK, "https://www.boot.dev")
    print(text_node)


main()