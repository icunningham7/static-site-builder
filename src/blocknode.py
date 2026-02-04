class BlockNode:
    def __init__(self, text, text_type):
        self.text = text
        self.text_type = text_type

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
        )
    
    def __repr__(self):
        return f"BlockNode({self.text}, {self.text_type})"
    