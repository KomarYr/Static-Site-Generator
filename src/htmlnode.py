


valid = str | None

class HTMLNode:
    def __init__(
            self, 
            tag: str | None = None, 
            value: str | None = None, 
            chlidren: list["HTMLNode"] | None = None,
            props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        if isinstance(self.props, dict):
            return " ".join(f' {key}="{value}"' for key, value in self.props.items())
        return ""


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
