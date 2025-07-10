from fasthtml.common import *
from monsterui.all import *
from blog_components import *

# Metadata for this pypost
metadata = {
    "title": "Reverse Infinite Scroll in FastHTML",
    "date": "2025-07-08", 
    "tags": ["TIL", "demo", "htmx", "fasthtml"],
    "draft": False
}

ar = APIRouter(prefix="/pyposts")
logs = [(f"Log", i) for i in range(1, 201)]

preview_md = """
Today I learned, how to build a *reverse* infinite scroll in FastHTML. 
I needed it to create a logviewer, where you want to see the latest logs, but also want to scroll up to see older entries.

Below you can see the final result, and after that I explain how I built it. 
"""

@ar
def rev_inf_scroll():
    return create_post_layout(metadata,
        Article(render_md(preview_md, class_map=custom_class_map), cls="pt-1 mb-6"),
        
        H2("Live Demo", cls="text-2xl font-bold text-slate-800 mb-4"),
        P("Here's the final working result - newest entries at the bottom, scroll up for older ones:", cls="text-slate-600 mb-4"),
        Div(
            Div(
                Table(
                    Thead(Tr(Th("Name"), Th("ID")), style="position: sticky; top: 0; background-color: white; z-index: 10;"),
                    Tbody(id="logs-body", hx_get=load_logs.to(page=1), hx_trigger="load")
                )
            ),
            style="max-height: 300px; overflow-y: scroll; border: 1px solid #ccc; display: flex; flex-direction: column-reverse;",
            id="demo-container"
        ),        
        Article(render_md("""\
## How it works

There's three parts to this solution.

### 1. Dynamically adding new rows as you scroll with HTMX

The standard pattern, scroll down, new items append at bottom, is easy with HTMX. 
Phihung's excellent [FastHTML + HTMX examples](https://huggingface.co/spaces/phihung/htmx_examples) has a live example. 
Super useful! Check it out if you haven't seen it before!

The key parts are the `hx_trigger="intersect once"` and `hx_swap="afterbegin"` which means that when the last row is revealed, the next page is loaded.

### 2. Reverse the container in CSS

To start at the bottom and scroll up, we need to add `display: flex; flex-direction: column-reverse;` to the container.
Below you can see an example that shows the effect of adding the CSS. You can toggle the CSS reversal by clicking the button.
"""
            , class_map=custom_class_map), cls="pt-6 mb-6"),
        toggle_css_demo(reversed=False),
        Article(render_md("""\
### 3. Reverse the data in Python

However, the CSS also flips the order of the items on the page. So we need to fix that.

We can do this by reversing the data in Python. Here's how I did it:

```python
def load_logs(page: int, limit: int = 5):
    page_logs = logs[-(page * limit):-(page - 1) * limit]  # <-- slice the logs array in reverse order
    if not page_logs: return []
    rows = [Tr(Td(name), Td(id)) for name, id in page_logs]
    rows.append(Tr(hx_trigger="intersect once", hx_swap="afterbegin", hx_get=load_logs.to(page=page + 1), hx_target="#logs-body", style="height: 1px; opacity: 0;"))
    return rows
```

## Putting it all together
Here you can see the full code all together.
```python
from fasthtml.common import *

app, rt = fast_app()
logs = [(f"Log", i) for i in range(1, 201)]  # <-- ok I lied, this example is not really "infinite"

@rt("/")
def get():
    return Container(
        H1("Reverse Infinite Scroll"),
        Div(
            Table(
                Thead(Tr(Th("Name"), Th("ID"))),
                Tbody(id="logs-body", hx_get="/load_logs?page=1", hx_trigger="load")
            ),
            # Key: CSS reversal to start at bottom
            style="max-height: 300px; overflow-y: scroll; border: 1px solid #ccc; display: flex; flex-direction: column-reverse;"
        )
    )

@rt("/load_logs")
def load_logs(page: int, limit: int = 5):
    # Key: Reverse data to get newest entries at the bottom
    page_logs = logs[-(page * limit):-(page - 1) * limit if page > 1 else None]
    if not page_logs: return []
    
    rows = [Tr(Td(name), Td(id)) for name, id in page_logs]
    # Key: `intersect once` and `afterbegin` for infinite scroll
    rows.append(Tr(hx_trigger="intersect once", hx_swap="afterbegin", 
                   hx_get=f"/load_logs?page={page + 1}", hx_target="#logs-body", 
                   style="height: 1px; opacity: 0;"))
    return rows

serve()
```
""", class_map=custom_class_map), cls="pt-6 mb-6"),
    )

def create_css_demo_lines(reversed_css=False):
    """Helper function to create the demo lines with optional CSS reversal"""
    style = "border: 1px solid #ccc; max-width: 200px; max-height: 300px; overflow-y: scroll;"
    if reversed_css: style += " display: flex; flex-direction: column-reverse;"
    return Div(
        *[Div(f"Line {i}", cls="p-2 border-b border-gray-200") for i in range(1, 200)],
        style=style,
        id="css-demo"
    )

@ar
def toggle_css_demo(reversed: bool = False):
    button_text = "Remove CSS Reversal" if reversed else "Apply CSS Reversal"
    
    return Div(
        Button(button_text, 
               hx_post=toggle_css_demo.to(reversed=not reversed), 
               hx_target="#css-demo-container", 
               hx_swap="outerHTML",
               cls="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mb-3"),
        create_css_demo_lines(reversed),
        id="css-demo-container"
    )

@ar
def load_logs(page: int, limit: int = 5):
    page_logs = logs[-(page * limit):-(page - 1) * limit if page>1 else None]
    if not page_logs: return []
    rows = [Tr(Td(name), Td(id)) for name, id in page_logs]
    rows.append(Tr(hx_trigger="intersect once", hx_swap="afterbegin", hx_get=load_logs.to(page=page + 1), hx_target="#logs-body", style="height: 1px; opacity: 0;"))
    return rows
