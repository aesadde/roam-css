import os
from dataclasses import dataclass

DEFAULT_BG_COLOR = "#fcdcaa"
DEFAULT_TEXT_COLOR = "#000000"

powerline_tag_style = """
    position: relative;
    padding: 3px 1.25rem;
    margin-right: -14px;
    cursor: pointer;
    clip-path: polygon(0% 0%, calc(100% - 14px) 0%, 100% 50%, calc(100% - 14px) 100%, 100% 100%, 0% 100%, 14px 50%);
    line-height: 2em;
    font-weight: 500;
    color: #000000;
    background-color: #1190ad; 
"""

def tag_style_with_color(color: str = DEFAULT_TEXT_COLOR, bg_color: str = DEFAULT_BG_COLOR) -> str:
  return """
    padding: 3px 7px;
    line-height: 2em;
    font-weight: 500;
    color: {0};
    background-color: {1};
    border-radius: 5px;
    """.format(color, bg_color)

default_before_style = """
 margin-right: .5em;
"""

def before_style_with_image(url: str) -> str: 
    lines = f'\nbackground-image: url("{url}");'
    lines += """
    background-size: cover;
    position: relative;
    display: inline-block;
    width: 14px;
    height: 12px;
    """
    return lines


@dataclass
class Tag:
    name: str
    emoji: object
    style: str = tag_style_with_color()
    before_style: str = default_before_style


category_tags = [
    Tag("Videos", "🎬"),
    Tag("Podcasts","🎧"),
    Tag("Articles","📑"),
    Tag("Books","📚"),
    Tag("People","📞"),
    Tag("Quotes",""),
    Tag("Projects","📁"),
    Tag("Tools", "⚒️"),
    Tag("Recipes","🥘"),
    Tag("Tweets", "", before_style=before_style_with_image("https://raw.githubusercontent.com/johan/svg-cleanups/master/logos/twitter.svg"))
]

workflow_tags = [
    Tag("To-Process","🔨", powerline_tag_style),
    Tag("To-Create","✍️", powerline_tag_style),
    Tag("In-Process","📝", powerline_tag_style),   
    Tag("To-Publish","🚀", powerline_tag_style),
    Tag("Ideas", "💡", powerline_tag_style)
]


todo_tags = [
    Tag("Scheduled", "", tag_style_with_color(bg_color="#9bd1dd")),
    Tag("Later","⏰", tag_style_with_color(bg_color="#9bd1dd"))
]


def generate_test_html():

    lines = ["<html>", "\n<body>", "\n<head>", '\n<link rel="stylesheet" type="text/css" href="./roam.css" media="screen" />', "\n</head>"]
    with open("test-tags.html", "w") as f:
        lines += "\n<h2>Category Tags</h2>"
        for t in category_tags:
            lines += f'\n<span data-tag="{t.name}" class="rm-page-ref rm-page-ref--tag">#{t.name}</span>'
            lines += "\n<br><br>"

        lines += "\n<h2>Workflow Tags</h2>"
        for t in workflow_tags:
            lines += f'\n<span data-tag="{t.name}" class="rm-page-ref rm-page-ref--tag">#{t.name}</span>'
            lines += "\n<br><br>"
            
        lines += "\n<h2>TODO Tags</h2>"
        for t in todo_tags:
            lines += f'\n<span data-tag="{t.name}" class="rm-page-ref rm-page-ref--tag">#{t.name}</span>'
            lines += "\n<br><br>"

        lines += ["\n</body>\n</html>"]
        f.writelines(lines)


def build_tag_css(tag : Tag) -> str:
    lines = f"\n/* {tag.name} */"
    lines += f'\n span.rm-page-ref[data-tag="{tag.name}"]' + " {"
    lines += tag.style
    lines += "\n}"

    ## css before tag

    lines += f'\nspan.rm-page-ref[data-tag="{tag.name}"]:before' + " {"
    lines += f'\ncontent: "{tag.emoji}";'
    lines += tag.before_style
    lines += "}"

    return lines


def generate_css_file(tags: list):
    lines = ["/* Autogenerated CSS Styles For Roam Tags And Links"]
    with open("roam.css", "w") as f:
        for t in tags: 
            lines += build_tag_css(t)
        f.writelines(lines)
           


generate_test_html()
generate_css_file(category_tags + workflow_tags + todo_tags)
