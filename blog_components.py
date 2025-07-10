from fasthtml.common import *
from monsterui.all import *
from monsterui.franken import LightboxContainer, LightboxItem, apply_classes
from datetime import datetime
import mistletoe

custom_class_map = {
    'h1': 'text-3xl font-bold text-slate-800 my-4',
    'h2': 'text-2xl font-bold text-slate-800 my-3',
    'h3': 'text-xl font-bold text-slate-800 my-2',
    'p': 'text-slate-600 my-2 leading-normal',
    'a': 'text-blue-600 hover:text-blue-800 underline',
    'ul': 'list-disc pl-5 my-3 text-slate-600',
    'ol': 'list-decimal pl-5 my-3 text-slate-600',
    'li': 'my-1',
    'blockquote': 'border-l-4 border-slate-300 pl-4 italic my-3 text-slate-600',
    'pre': 'bg-slate-100 p-4 rounded my-3 overflow-auto',
    'code': 'bg-slate-100 px-1 py-0.5 rounded text-sm font-mono',
    'hr': 'my-4 border-t border-slate-200',
    'table': 'w-full border-collapse my-3',
    'th': 'border border-slate-300 px-4 py-2 bg-slate-100 text-left',
    'td': 'border border-slate-300 px-4 py-2',
    'strong': 'font-bold',
    'em': 'italic'
}

class BlogRenderer(mistletoe.HTMLRenderer):
    def __init__(self, img_dir=None):
        super().__init__()
        self.img_dir = img_dir
        
    def render_image(self, token):
        src = token.src
        alt = token.children[0].content if token.children else ''
        title = token.title if hasattr(token, 'title') else alt
        
        if self.img_dir and not src.startswith(('http://', 'https://', '/')):
            clean_img_dir = self.img_dir.lstrip('./')
            src = f'/{clean_img_dir}/{src}'
        
        figure = Div(
            LightboxContainer(
                LightboxItem(
                    Img(src=src, alt=alt, cls="lightbox-img rounded", loading="lazy"),
                    href=src,
                    data_alt=alt,
                    data_caption=title or alt
                ),
                data_uk_lightbox="animation: slide; caption-position: bottom"
            ),
            cls="lightbox-container",
            style="width: 50%; margin: 1rem auto;"
        )
        
        return str(figure)

def render_md(md_content:str, class_map=None, class_map_mods=None, img_dir:str=None):
    if md_content == '': return md_content
    
    class CustomRenderer(BlogRenderer):
        def __init__(self):
            super().__init__(img_dir=img_dir)
    
    html_content = mistletoe.markdown(md_content, CustomRenderer)
    
    effective_class_map = class_map if class_map is not None else custom_class_map
    if class_map_mods: effective_class_map = {**effective_class_map, **class_map_mods}
    
    return NotStr(apply_classes(html_content, effective_class_map))

def create_site_header():
    return Div(DivFullySpaced(H1(A("Rens' Blog", href="/"), cls="text-2xl font-bold text-slate-800 hover:text-blue-600"), Form(Div(UkIcon("search", cls="text-slate-400"), Input(name="q", placeholder="Search...", cls="border-0 focus:ring-0 text-sm w-32"), cls="flex items-center gap-1 border rounded px-2 py-1"), action="/search", method="get")), cls="border-b border-slate-200 py-4 mb-3")

def create_site_footer():
    return Footer(DivFullySpaced(P("© 2025 Rens' Blog. All rights reserved.", cls="text-xs text-slate-500"), DivLAligned(*[UkIconLink(icon, cls="text-slate-600 hover:text-blue-600") for icon in ["twitter", "github", "linkedin"]], cls="gap-3")), cls="py-3 mt-6 border-t border-slate-200")

def format_pretty_date(date_str):
    try: return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")
    except: return date_str

def create_date_divider(date):
    return Div(DividerSplit(Small(format_pretty_date(date), cls="text-slate-600 text-xs font-light px-3 bg-white")), cls="my-6")

def Tags(tags):
    return DivLAligned(*[Label(A(tag, href=f"/tags/{tag}", cls="text-slate-600 hover:text-blue-600")) for tag in tags], cls="gap-1 mt-1")

def create_pypost_layout(metadata, *content):
    """Create standard pypost layout with header, title, date, content, tags, and footer"""
    return Container(
        create_site_header(),
        DivFullySpaced(
            A(DivLAligned(UkIcon("arrow-left", cls="text-blue-600 h-4 w-4 mr-2"), Span("Back to posts", cls="text-blue-600")), href="/", cls="inline-flex items-center text-sm hover:text-blue-800"),
            cls="mb-3 items-center"
        ),
        H1(metadata["title"], cls="text-3xl font-bold text-slate-800 mt-3 mb-3"),
        create_date_divider(metadata["date"]),
        *content,
        Tags(metadata["tags"]),
        create_site_footer(),
        cls="max-w-4xl mx-auto"
    )
