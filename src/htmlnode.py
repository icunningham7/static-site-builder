class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        props_html = ""
        if self.props:
            for key, value in self.props.items():
                props_html += f' {key}="{value}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
    def __eq__(self, other):
        if (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
        ):
            if self.children is None and other.children is None:
                return True
            
            if self.children is None or other.children is None:
                return False

            if self.children and other.children:
                if len(self.children) != len(other.children):
                    return False
                
                for i, child in enumerate(self.children):
                    if not child == other.children[i]:
                        return False
                    
        return True



class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError

        if self.tag is None:
            return self.value

        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: a tag is required.")

        if not self.children:
            raise ValueError("invalid ParentNode: children are required.")

        children_nodes = ""
        for child in self.children:
            children_nodes += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_nodes}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
    def __eq__(self, other):
        if self.tag != other.tag:
            return False
        
        if self.props != other.props:
            return False
    
        if self.children is None and other.children is None:
            return True
    
        if self.children is None or other.children is None:
            return False

        if self.children and other.children:
            if len(self.children) != len(other.children):
                return False
            for i, child in enumerate(self.children):
                if not child == other.children[i]:
                    return False
                

        return True