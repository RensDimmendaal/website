import json
import yaml
from fastcore.all import *
from fasthtml.common import *
from monsterui.all import *
from monsterui.franken import LightboxContainer, LightboxItem, apply_classes
from datetime import datetime
import mistletoe
from mistletoe.span_token import Image

# CSS for lightbox images
lightbox_css = """
.uk-lightbox { z-index: 1010; }
.lightbox-container {
  width: 50% !important;
  margin: 1rem auto !important;
  display: block !important;
}
img.lightbox-img {
  width: 100% !important;
  height: auto !important;
  cursor: pointer;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
img.lightbox-img:hover { transform: scale(1.02); }
@media (max-width: 768px) {
  .lightbox-container { width: 80% !important; }
}
"""

# Use MonsterUI's theme system
app, rt = fast_app(
    pico=False, 
    hdrs=(*Theme.blue.headers(highlightjs=True),),
    styles=[lightbox_css]
)

# Custom class map for blog styling
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

# Custom markdown renderer with lightbox for images
class BlogRenderer(mistletoe.HTMLRenderer):
    def __init__(self, img_dir=None):
        super().__init__()
        self.img_dir = img_dir
        
    def render_image(self, token):
        src = token.src
        alt = token.children[0].content if token.children else ''
        title = token.title if hasattr(token, 'title') else alt
        
        # Handle relative paths
        if self.img_dir and not src.startswith(('http://', 'https://', '/')):
            src = f'{self.img_dir}/{src}'
        
        # Create container with lightbox functionality
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
            style="width: 50%; margin: 1rem auto;"  # Critical for correct sizing
        )
        
        return str(figure)

def render_md(md_content:str, class_map=None, class_map_mods=None, img_dir:str=None):
    """Renders markdown with lightbox-enabled images."""
    if md_content == '': return md_content
    
    # Create renderer with img_dir
    class CustomRenderer(BlogRenderer):
        def __init__(self):
            super().__init__(img_dir=img_dir)
    
    html_content = mistletoe.markdown(md_content, CustomRenderer)
    
    effective_class_map = class_map if class_map is not None else custom_class_map
    if class_map_mods:
        effective_class_map = {**effective_class_map, **class_map_mods}
    
    return NotStr(apply_classes(html_content, effective_class_map))

def load_post(fp:Path):
    content = fp.read_text()
    if content.startswith("---\n"): 
        _, post, *content = content.split("---\n")
        post = yaml.safe_load(post)
        post['content'] = "---\n".join(content)
        post['fname'] = fp.stem
    else: raise NotImplementedError("No metadata found in post")
    return post

# @flexicache(mtime_policy("./posts"))
def all_posts(): return [load_post(fp) for fp in Path("./posts/").glob("*.md")]

def Tags(tags):
    """Create compact tags with muted styling."""
    return DivLAligned(
        *[Label(
            A(tag, href=f"/tags/{tag}", cls="text-slate-600 hover:text-blue-600"),
          ) for tag in tags], 
        cls="gap-1 mt-1"
    )

def format_pretty_date(date_str):
    """Convert a date string from YYYY-MM-DD to a human-friendly format."""
    try: return datetime.strptime(date_str, "%Y-%m-%d").strftime("%B %d, %Y")
    except: return date_str

def create_date_divider(date):
    """Create a date divider with centered text within a line."""
    return Div(
        DividerSplit(
            Small(format_pretty_date(date), cls="text-slate-600 text-xs font-light px-3 bg-white")
        ),
        cls="my-6"
    )


def create_site_header():
    """Create the consistent site header with navigation."""
    return Div(
        DivFullySpaced(
            H1(A("Rens' Blog", href="/"), cls="text-2xl font-bold text-slate-800 hover:text-blue-600"),
            Div(
                *[A(label, href=f"/{label.lower()}", 
                    cls="mx-3 text-slate-600 hover:text-blue-600 transition-colors last:mr-0") 
                  for label in ["About", "Archive", "Contact"]],
                cls="flex items-center"
            )
        ),
        cls="border-b border-slate-200 py-4 mb-3"
    )


def create_site_footer():
    """Create the consistent site footer with copyright and social links."""
    return Footer(
        DivFullySpaced(
            P("© 2025 Rens' Blog. All rights reserved.", cls="text-xs text-slate-500"),
            DivLAligned(
                *[UkIconLink(icon, cls="text-slate-600 hover:text-blue-600") 
                  for icon in ["twitter", "github", "linkedin"]],
                cls="gap-3"
            ),
        ),
        cls="py-3 mt-6 border-t border-slate-200"
    )


def create_article_card(post, is_last=False):
    """Create a compact newspaper-like article in single column."""
    # Don't add bottom border for the last article in a group
    border_class = "" if is_last else "border-b border-slate-200"
    
    # Use the post's fname as the URL slug
    url_slug = post["fname"]
    
    content = post['content']
    keep_reading = Div()
    if "## " in content: 
        content = content.split("## ")[0].strip()
        keep_reading = A(
                DivLAligned(
                    UkIcon("corner-down-right", cls="text-blue-600 mr-1"),
                    Small("Keep reading", cls="text-blue-600"),
                ),
                href=f"/posts/{url_slug}",
                cls="text-sm"
            )

    return Article(
        H4(
            A(
                post["title"],
                href=f"/posts/{url_slug}",
                cls="text-slate-800 hover:text-blue-600"
            )
        ),
        render_md(content, class_map=custom_class_map, img_dir="./posts/"),
        DivFullySpaced(
            keep_reading,
            Tags(post.get("tags",["Untagged"])),
        ),
        cls=f"mb-4 pb-2 {border_class}"
    )


def create_search_and_categories():
    """Create a compact header with search and categories."""
    return Div(
        Div(
            UkIcon("search", cls="text-slate-400"),
            Input(placeholder="Search...", cls="border-0 focus:ring-0"),
            cls="flex items-center gap-2 border rounded px-2 py-1 mb-3"
        ),
        # Div(
        #     DivLAligned(
        #         *[Button(cat, cls=ButtonT.secondary) for cat in ["Food", "Travel", "Tech", "Life"]],
        #         cls="gap-2"
        #     ),
        # ),
        cls="mb-4"
    )


def create_centered_heading(title:str):
    """Create a heading with a line perfectly centered through the text."""
    return Div(
        DividerSplit(
            H2(title, cls="text-xl font-bold px-4 bg-white text-slate-800")
        ),
        cls="my-8"
    )

@rt("/posts/{fname}")
def posts(fname:str):
    """Display an individual blog post from a markdown file."""

    if p:=first(p for p in all_posts() if p['fname'] == fname): pass
    else: return Container(
            create_site_header(),
            H1("Post Not Found", cls="text-2xl font-bold text-red-600 my-8"),
            P(f"The post '{fname}' could not be found.", cls="text-slate-600"),
            Br(),
            A("Return to Home", href="/", cls="text-blue-600 hover:underline"),
            create_site_footer(),
            cls=ContainerT.sm
        )
        
    rendered_content = render_md(p['content'], class_map=custom_class_map)
    return Container(
        # Use reusable header
        create_site_header(),
        
        # Back to posts link with tags right-aligned
        DivFullySpaced(
            A(
                DivLAligned(
                    UkIcon("arrow-left", cls="text-blue-600 h-4 w-4 mr-2"),
                    Span("Back to posts", cls="text-blue-600"),
                ),
                href="/",
                cls="inline-flex items-center text-sm hover:text-blue-800"
            ),
            cls="mb-3 items-center"
        ),
        
        H1(p['title'], cls="text-3xl font-bold text-slate-800 mt-3 mb-3"),
        
        # Date divider
        create_date_divider(p['date']),
        
        # Main content
        Article(
            rendered_content,
            cls="pt-1 mb-6"
        ),
        
        # Tags at the bottom of the article
        Tags(p.get('tags', [])),
        
        # Use reusable footer
        create_site_footer(),
        
        cls=ContainerT.sm,
    )

@rt("/")
def index():
    """Homepage for the blog with single column newspaper-inspired density."""
    # Group posts by date
    posts_by_date = {}
    for post in all_posts():
        date = post.get('date')
        if date not in posts_by_date:
            posts_by_date[date] = []
        posts_by_date[date].append(post)
    
    # Sort dates in descending order
    sorted_dates = sorted(posts_by_date.keys(), reverse=True)
    
    # Create article components
    articles = []
    
    for date in sorted_dates:
        articles.append(create_date_divider(date))
        
        # Articles for this date in a single column
        posts = posts_by_date[date]
        for i, post in enumerate(posts):
            # Mark the last post in each date group
            is_last = (i == len(posts) - 1)
            articles.append(create_article_card(post, is_last))

    # Container with newspaper-inspired layout in single column
    return Container(
        create_site_header(),
        create_search_and_categories(),
        create_centered_heading("Latest Posts"),
        # Main content with single column layout
        Main(
            *articles,
            cls="mb-6"
        ),
        create_site_footer(),
        cls=ContainerT.sm,
    )

@rt("/tags/{tag}")
def tags(tag:str):
    """Display all posts with a specific tag."""
    # Group posts by date
    posts_by_date = {}
    for post in all_posts():
        if tag in post.get('tags', []):
            date = post.get('date')
            if date not in posts_by_date:
                posts_by_date[date] = []
            posts_by_date[date].append(post)
    
    # Sort dates in descending order
    sorted_dates = sorted(posts_by_date.keys(), reverse=True)
    
    # Create article components
    tagged_articles = []
    
    for date in sorted_dates:
        tagged_articles.append(create_date_divider(date))
        
        # Add each matching post
        posts = posts_by_date[date]
        for i, post in enumerate(posts):
            is_last = (i == len(posts) - 1)
            tagged_articles.append(create_article_card(post, is_last))
    
    return Container(
        create_site_header(),
        create_search_and_categories(),
        create_centered_heading(f"Posts Tagged: {tag}"),
        
        # Main content
        Main(
            *tagged_articles if tagged_articles else [
                P("No posts found with this tag.", cls="text-center text-slate-600 my-12")
            ],
            cls="mb-6"
        ),
        
        create_site_footer(),
        cls=ContainerT.sm,
    )


serve()
