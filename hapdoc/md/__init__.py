# -*- coding: utf-8 -*-
"""
Provides Markdown to Html code translator
"""
from re import MULTILINE, findall, sub, compile
from secrets import token_hex


class Md2Html:
    """
    Provides Markdown to Html
    """
    _rules = [
        # > -> &gt
        (r'>', r'&gt', 1),
        (r'<', r'&lt', 1),
        # <br>
        (compile(r'( {2}$(?!\s*`))', MULTILINE), r'<br>', 1),
        # Line
        (compile(r'^\s*^(_{3,}|-{3})\s*', MULTILINE), r'<hr>', 1),
        # List
        (
            compile(r'^((\s*-\s*[^\n]+(?= *\n))+)', MULTILINE),
            r'<ul style="list-style-type: disc">\n\1</ul>', 1
        ),
        (compile(r'\n+-\s*([^\n]+)', MULTILINE), r'<li>\1</li>', 1),
        # Headers
        (compile(r'^###### *([^\n]+)', MULTILINE), r'<h6 class="titleRef">\1</h6>', 1),
        (compile(r'^##### *([^\n]+)', MULTILINE), r'<h5 class="titleRef">\1</h5>', 1),
        (compile(r'^#### *([^\n]+)', MULTILINE), r'<h4 class="titleRef">\1</h4>', 1),
        (compile(r'^### *([^\n]+)', MULTILINE), r'<h3 class="titleRef">\1</h3>', 1),
        (compile(r'^## *([^\n]+)', MULTILINE), r'<h2 class="titleRef">\1</h2>', 1),
        (compile(r'^# *([^\n]+)', MULTILINE), r'<h1 class="titleRef">\1</h1>', 1),
        # Image
        (r'!\[([^\n\]]+)\]\(([^\)\s]+)\)', r'<img src="\2" alt="\1">', 1),
        # URL
        (r'\[([^\n\]]+)\]\(([^\)\s]+)\)', r'<a href="\2">\1</a>', 1),
        # Code
        (
            r'```(\S+)\s*([\s\S]+?)```',
            r'<pre><button class="flex gap-2 items-center text-white"><p>Copy code</p><i class="fas fa-copy"></i>'
            r'</button><code class="language-\1">\2</code></pre>',
            1
        ),
        (r'(?!")`([^`"]+)`(?!")', r'<code class="command">\1</code>', 1),
        # Bold
        (r'[\s]\*\*([^*]*)\*\*[\s]', r'<b>\1</b>', 1),
        (r'[\s]__([^_]*)__[\s]', r'<b>\1</b>', 1),
        # Italic
        (r'[\s]\*([^*]*)\*[\s]', r'<em>\1</em>', 1),
        (r'[\s]_([^_]*)_[\s]', r'<em>\1</em>', 1),
        # Find text without element
        # (r'(<\/(pre|h\d))>([\s\S]+?)<(\/?)(?=hr|div|pre|h\d|ul)', r'\1><p>\3</p><\4', 1),
        (r'(<\/?)(div|ul|hr)([^>]*>)([\s\S]*?)(<\/?)(p|div|h\d)', r'\1\2\3<p>\4</p>\5\6', 1),
    ]

    @staticmethod
    def cast(source: str) -> str:
        """
        Casts Markdown sources to HTML code
        :param source: Markdown sources
        """
        for pattern, repl, repeat_count in Md2Html._rules:
            for _ in range(repeat_count):
                source = sub(pattern, repl, source)
        return Md2Html._prepare_blockquotes(source)

    @staticmethod
    def rand_title_ref(html_source: str) -> tuple[str, list[dict]]:
        result = []
        for level, attrs, text in findall(r'<h(\d)([^>]+?)>([^<]+?|[^h]+?)</h\1', html_source):
            random_id = token_hex(8)
            result.append({
                'id': random_id,
                'title': text,
                'level': int(level)
            })
            html_source = html_source.replace(
                f'<h{level}{attrs}>{text}',
                f'<h{level}{attrs} id="{random_id}">{text}',
                1
            )
        return html_source, result

    @staticmethod
    def _prepare_blockquotes(source: str) -> str:
        # Blockquote
        blockquotes = findall(r'((^&gt\s*[^\n]+[\n\r]*)+)', source, MULTILINE)
        for blockquote, _ in blockquotes:
            print(blockquote)
            new_blockquote = sub(r'^ *&gt\s*', r'', blockquote, MULTILINE)
            new_blockquote = sub(r'\n *&gt\s*', r'\n', new_blockquote, MULTILINE)
            new_blockquote = sub(r'>[\n ]*&gt\s*', r'>', new_blockquote, MULTILINE)
            source = source.replace(blockquote, f'<div class="quote">{new_blockquote}</div>')
            print(new_blockquote)
        if findall(r'((^&gt\s*[^\n]+[\n\r]*)+)', source, MULTILINE):
            return Md2Html._prepare_blockquotes(source)
        return source
