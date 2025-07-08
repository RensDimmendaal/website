import yaml, tantivy, random
from fastcore.all import *
from fasthtml.common import *
from monsterui.all import *
from datetime import datetime
from functools import cache
from collections import Counter

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



def load_post(fp:Path):
    content = fp.read_text()
    if content.startswith("---\n"): 
        _, post, *content = content.split("---\n")
        post = yaml.safe_load(post)
        post['content'] = "---\n".join(content)
        post['fname'] = fp.stem
        post['draft'] = post.get('draft', False)
    else: raise NotImplementedError("No metadata found in post")
    return post

@cache
def all_posts(): return [load_post(fp) for fp in Path("./posts/").glob("*.md")]

def published_posts(): return [p for p in all_posts() if not p.get('draft', False)]

def load_pypost(fp:Path):
    content = fp.read_text()
    if content.startswith('"""') and '---' in content:
        docstring_end = content.find('"""', 3)
        docstring = content[3:docstring_end]
        _, meta, _ = docstring.split('---')
        post = yaml.safe_load(meta)
        post['fname'] = fp.stem
        post['draft'] = post.get('draft', False)
        post['is_pypost'] = True
        module = importlib.import_module(f"pyposts.{fp.stem}")
        post['preview_content'] = module.preview_md
        return post
    return None

@cache
def all_pyposts(): return [p for p in [load_pypost(fp) for fp in Path("./pyposts/").glob("*.py") if fp.stem != "__init__"] if p]

def published_pyposts(): return [p for p in all_pyposts() if not p.get('draft', False)]

@cache
def top_tags(n=5): return Counter(tag for p in published_posts() for tag in p.get('tags', [])).most_common(n)

def create_search_index():
    schema_builder = tantivy.SchemaBuilder()
    schema_builder.add_text_field("title", stored=True)
    schema_builder.add_text_field("body", stored=True, tokenizer_name='en_stem')
    schema_builder.add_text_field("tags", stored=True)
    schema_builder.add_text_field("fname", stored=True)
    schema = schema_builder.build()
    index = tantivy.Index(schema)
    writer = index.writer()
    for post in published_posts():
        writer.add_document(tantivy.Document(
            title=[post['title']],
            body=[post['content']],
            tags=[' '.join(post.get('tags', []))],
            fname=[post['fname']]
        ))
    writer.commit()
    writer.wait_merging_threads()
    return index

search_index = create_search_index()




from blog_components import create_site_header, create_site_footer, create_date_divider, format_pretty_date, Tags, render_md, custom_class_map

def create_bio_section():
    "Create bio section with random banner image"
    banner_imgs = ["fish.jpg", "man.jpg", "tree.jpg"]
    selected_img = random.choice(banner_imgs)
    return Div(
        Img(src=f"/static/{selected_img}", cls="w-full h-48 object-contain mb-4"),
        Div(
            P("I'm Rens Dimmendaal, a member of technical staff at ", A("Answer.AI", href="https://answer.ai", cls="text-blue-600 hover:text-blue-800 underline"), " a new kind of AI R&D Lab. I write about the things I learn.", 
              cls="text-slate-700 text-sm leading-relaxed mb-0"),
            cls="bg-slate-50 border-l-4 border-blue-500 p-4 rounded-r"
        ),
        cls="mb-6"
    )


def create_article_card(post, is_last=False):
    border_class = "" if is_last else "border-b border-slate-200"
    url_slug = post["fname"]
    
    if post.get('is_pypost'):
        content = post['preview_content']
        href = f"/{url_slug}"
        keep_reading = A(DivLAligned(UkIcon("play", cls="text-blue-600 mr-1"), Small("Try demo", cls="text-blue-600")), href=href, cls="text-sm")
    else:
        content = post['content']
        keep_reading = Div()
        if "## " in content: 
            content = content.split("## ")[0].strip()
            keep_reading = A(DivLAligned(UkIcon("corner-down-right", cls="text-blue-600 mr-1"), Small("Keep reading", cls="text-blue-600")), href=f"/posts/{url_slug}", cls="text-sm")
        href = f"/posts/{url_slug}"

    return Article(
        H4(A(post["title"], href=href, cls="text-slate-800 hover:text-blue-600")),
        render_md(content, class_map=custom_class_map, img_dir="./posts/"),
        DivFullySpaced(keep_reading, Tags(post.get("tags",["Untagged"]))),
        cls=f"mb-4 pb-2 {border_class}"
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
    return Container(
        create_site_header(),
        create_bio_section(), 
        create_centered_heading("Latest Posts"),
        Main(id="posts-container", cls="mb-6"),
        Div(hx_get="/posts-page/0", hx_trigger="load", hx_target="#posts-container"),
        create_site_footer(),
        cls=ContainerT.sm,
    )

@rt("/posts-page/{page}")
def posts_page(page:int):
    posts_per_page = 5
    all_posts_list = sorted(published_posts() + published_pyposts(), key=lambda p: p.get('date', ''), reverse=True)
    start_idx = page * posts_per_page
    end_idx = start_idx + posts_per_page
    page_posts = all_posts_list[start_idx:end_idx]
    
    if not page_posts: return ""
    
    posts_by_date = {}
    for post in page_posts:
        date = post.get('date')
        if date not in posts_by_date: posts_by_date[date] = []
        posts_by_date[date].append(post)
    
    sorted_dates = sorted(posts_by_date.keys(), reverse=True)
    articles = []
    
    for date in sorted_dates:
        articles.append(create_date_divider(date))
        posts = posts_by_date[date]
        for i, post in enumerate(posts): articles.append(create_article_card(post, i == len(posts) - 1))
    
    has_more = end_idx < len(all_posts_list)
    if has_more: articles.append(Div(hx_get=f"/posts-page/{page + 1}", hx_trigger="intersect once", hx_target="this", hx_swap="outerHTML"))
    
    return articles

@rt("/search")
def search(q:str=""):
    if not q: return RedirectResponse("/")
    searcher = search_index.searcher()
    query = search_index.parse_query(q, ["title", "body", "tags"])
    results = searcher.search(query, 20)
    matching_posts = [first(p for p in published_posts() if p['fname'] == searcher.doc(hit[1])['fname'][0]) for hit in results.hits]
    posts_by_date = {}
    for post in matching_posts:
        date = post.get('date')
        if date not in posts_by_date: posts_by_date[date] = []
        posts_by_date[date].append(post)
    sorted_dates = sorted(posts_by_date.keys(), reverse=True)
    search_articles = []
    for date in sorted_dates:
        search_articles.append(create_date_divider(date))
        posts = posts_by_date[date]
        for i, post in enumerate(posts):
            search_articles.append(create_article_card(post, i == len(posts) - 1))
    return Container(
        create_site_header(),
        create_centered_heading(f"Search Results: {q}"),
        Main(*search_articles if search_articles else [P("No posts found matching your search.", cls="text-center text-slate-600 my-12")], cls="mb-6"),
        create_site_footer(),
        cls=ContainerT.sm,
    )

@rt("/tags/{tag}")
def tags(tag:str):
    """Display all posts with a specific tag."""
    # Group posts by date
    posts_by_date = {}
    for post in published_posts():
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


import importlib
from pathlib import Path

for py_file in Path("pyposts").glob("*.py"):
    if py_file.stem != "__init__":
        print(f"Loading module: {py_file.stem}")
        try:
            module = importlib.import_module(f"pyposts.{py_file.stem}")
            if hasattr(module, 'ar'): 
                print(f"Adding routes from {py_file.stem}")
                module.ar.to_app(app)
        except Exception as e:
            print(f"Error loading {py_file.stem}: {e}")

print("Registered routes:")
for route in app.routes: print(f"  {route.methods} {route.path}")

serve()
