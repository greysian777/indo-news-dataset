from dataclasses import dataclass

@dataclass
class News:
    title: str
    link: str
    category: str
    paragraf: str=None

@dataclass
class Link():
    date_list: set
    berita: News