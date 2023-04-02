# -*- coding: utf-8 -*-
"""
Provides Markdown to Html code translator
"""
import re
from secrets import token_hex


class Md2Html:
    """
    Provides Markdown to Html
    """
    _rules = [
        (r'>', r'&gt', 0, 1),
        # Line
        (r'_{3,}\s*', r'<hr>', 0, 1),
        (r'-{3,}\s*', r'<hr>', 0, 1),
        # List
        (
            re.compile(r'^((\s*-\s*[^\n]+\n*)+)', re.MULTILINE),
            r'<ul style="list-style-type: disc">\n\1</ul>', re.MULTILINE, 1
        ),
        (re.compile(r'\n+-\s*([^\n]+)', re.MULTILINE), r'<li>\1</li>', re.MULTILINE, 1),
        # Headers
        (re.compile(r'^###### *([^\n]+)', re.MULTILINE), r'<h6 class="titleRef">\1</h6>', re.MULTILINE, 1),
        (re.compile(r'^##### *([^\n]+)', re.MULTILINE), r'<h5 class="titleRef">\1</h5>', re.MULTILINE, 1),
        (re.compile(r'^#### *([^\n]+)', re.MULTILINE), r'<h4 class="titleRef">\1</h4>', re.MULTILINE, 1),
        (re.compile(r'^### *([^\n]+)', re.MULTILINE), r'<h3 class="titleRef">\1</h3>', re.MULTILINE, 1),
        (re.compile(r'^## *([^\n]+)', re.MULTILINE), r'<h2 class="titleRef">\1</h2>', re.MULTILINE, 1),
        (re.compile(r'^# *([^\n]+)', re.MULTILINE), r'<h1 class="titleRef">\1</h1>', re.MULTILINE, 1),
        # Image
        (r'!\[([^\n\]]+)\]\(([^\)\s]+)\)', r'<img src="\2" alt="\1">', 0, 1),
        # URL
        (r'\[([^\n\]]+)\]\(([^\)\s]+)\)', r'<a href="\2">\1</a>', 0, 1),
        # Code
        (
            r'```(\S+)\s*([^`]+?)```',
            r'<pre><button>Copy code <?xml version="1.0" encoding="utf-8"?>'
            r'<svg width="24px" height="24px" viewBox="0 0 24 24" '
            r'xmlns="http://www.w3.org/2000/svg" style="display: inline">'
            r'<path clip-rule="evenodd" d="m7.37971 5.83706c-.'
            r'85075.24354-1.49225.97131-1.61046 1.86926-'
            r'.01764.13392-.01925.30542-.01925.79368v7.7c0 .8525.'
            r'00058 1.4467.03838 1.9093.03708.4539.10621.7147'
            r'.20685.9122.21572.4233.55992.7675.98329.9833.19752.1'
            r'006.45828.1697.91216.2068.46263.0378 1.05686.0384'
            r' 1.90932.0384h6.2c1.2426 0 2.25-1.0074 2.25-2.25v-1c0-'
            r'.4142.3358-.75.75-.75s.75.3358.75.75v1c0 2.0711'
            r'-1.6789 3.75-3.75 3.75h-6.2-.03213c-.81283 0-1.46844 0'
            r'-1.99934-.0434-.54664-.0446-1.02678-.139-1.471'
            r'-.3653-.7056-.3595-1.27928-.9332-1.63881-1.6388-.22634'
            r'-.4443-.3207-.9244-.36536-1.471-.04338-.5309-.'
            r'04337-1.1866-.04336-1.9994v-.0321-7.7l-.00001-.05786c-'
            r'.00007-.40868-.00011-.68702.03209-.93161.21389-'
            r'1.62466 1.45558-2.91505 3.05547-3.20159.30652-1.18429 '
            r'1.38234-2.05894 2.66245-2.05894h4c1.2801 0 2.355'
            r'9.87465 2.6624 2.05894 1.5999.28654 2.8416 1.57693 3.05'
            r'55 3.20159.0322.24459.0322.52292.0321.93158v.00'
            r'003.05786 2.5c0 .4142-.3358.75-.75.75s-.75-.3358-.75-.7'
            r'5v-2.5c0-.48826-.0016-.65976-.0193-.79368-.1182'
            r'-.89795-.7597-1.62572-1.6104-1.86926-.3541 1.10947-1.39'
            r'34 1.91294-2.6203 1.91294h-4c-1.22691 0-2.26617'
            r'-.80347-2.62029-1.91294zm1.37029-.83706c0-.69036.55964-'
            r'1.25 1.25-1.25h4c.6904 0 1.25.55964 1.25 1.25s-'
            r'.5596 1.25-1.25 1.25h-4c-.69036 0-1.25-.55964-1.25-1.25'
            r'zm3.8356 4.53148c-.2587-.32345-.7307-.37589-1.05'
            r'41-.11713l-.3148.25183-.028.02237c-.777.62165-1.39894 1'
            r'.11915-1.85949 1.55905-.47045.4494-.83594.896-1'
            r'.03856 1.4369-.31775.8482-.31775 1.7828 0 2.631.20262.5'
            r'409.56811.9875 1.03856 1.4369.46054.4399 1.0824'
            r'9.9374 1.85949 1.559v.0001l.028.0223.3148.2519c.3234.25'
            r'87.7954.2063 1.0541-.1172.2588-.3234.2064-.7954'
            r'-.1171-1.0542l-.3148-.2518c-.8114-.6491-1.3812-1.1059-1'
            r'.7884-1.4948-.40282-.3847-.58268-.6454-.66998-.'
            r'8784-.00489-.0131-.00966-.0262-.0143-.0393h9.31898c.414'
            r'2 0 .75-.3358.75-.75s-.3358-.75-.75-.75h-9.3189'
            r'8c.00464-.0131.00941-.0262.0143-.0393.0873-.233.26716-.'
            r'4937.66998-.8784.4072-.3889.977-.8457 1.7884-1.'
            r'4948l.3148-.2518c.3235-.2588.3759-.73077.1171-1.05422z"'
            r' fill="#ffffff" fill-rule="evenodd"/></svg>'
            r'</button><code class="language-\1">\2</code></pre>',
            0, 1
        ),
        (r'(?!")`([^`"]+)`(?!")', r'<code class="command">\1</code>', 0, 1),
        # Bold
        (r'[\s]\*\*([^*]*)\*\*[\s]', r'<b>\1</b>', 0, 1),
        (r'[\s]__([^_]*)__[\s]', r'<b>\1</b>', 0, 1),
        # Italic
        (r'[\s]\*([^*]*)\*[\s]', r'<em>\1</em>', 0, 1),
        (r'[\s]_([^_]*)_[\s]', r'<em>\1</em>', 0, 1),
        # Find text without element
        (r'(<\/(pre|h\d))>([\s\S]+?)<(\/?)(?=hr|div|pre|h\d|ul)', r'\1><p>\3</p><\4', 0, 1)
    ]

    @staticmethod
    def cast(source: str) -> str:
        """
        Casts Markdown sources to HTML code
        :param source: Markdown sources
        """
        for pattern, repl, flags, repeat_count in Md2Html._rules:
            for _ in range(repeat_count):
                source = re.sub(pattern, repl, source, flags)
        return Md2Html._prepare_blockquotes(source)

    @staticmethod
    def rand_title_ref(html_source: str) -> tuple[str, list[dict]]:
        result = []
        for level, attrs, text in re.findall(r'<h(\d)([^>]+?)>([^<]+?|[^h]+?)</h\1', html_source):
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
        blockquotes = re.findall(r'((^&gt\s*[^\n]+[\n\r]*)+)', source, re.MULTILINE)
        for blockquote, _ in blockquotes:
            print(blockquote)
            new_blockquote = re.sub(r'^ *&gt\s*', r'', blockquote, re.MULTILINE)
            new_blockquote = re.sub(r'\n *&gt\s*', r'\n', new_blockquote, re.MULTILINE)
            new_blockquote = re.sub(r'>[\n ]*&gt\s*', r'>', new_blockquote, re.MULTILINE)
            source = source.replace(blockquote, f'<div class="quote">{new_blockquote}</div>')
            print(new_blockquote)
        if re.findall(r'((^&gt\s*[^\n]+[\n\r]*)+)', source, re.MULTILINE):
            return Md2Html._prepare_blockquotes(source)
        return source
