import logging
import MeCab
import ipadic
import os
import re


logger = logging.getLogger(__name__)


class TTStranslation:
    chunk_buffer = ""

    def __init__(self, table_name="default_translation.txt"):
        self.logger = logging.getLogger(__name__)
        self.mecab = MeCab.Tagger(ipadic.MECAB_ARGS)
        self.translation_table = {}
        path = os.path.dirname(os.path.abspath(__file__))
        if table_name:
            try:
                with open(os.path.join(path, table_name)) as f:
                    translist = f.readlines()
                    logger.warning(f"read translation rules = {translist}")
            except Exception as e:
                translist = []

            for rule in translist:
                lhsrhs = rule.split(":")
                if len(lhsrhs) > 1:
                    self.translation_table[lhsrhs[0]] = lhsrhs[1].strip()
                else:
                    self.translation_table[lhsrhs[0]] = ""

    def sota_translation(self, content: str) -> str:
        content = re.sub(r"\*\*", "", content)
        content = self.remove_urls_from_chunk(content)
        content_lines = content.split("\n")
        translation_result = []

        for line in content_lines:
            nodes = []
            node = self.mecab.parseToNode(line)
            prev = ""
            while node:
                s: str = node.surface
                if s.isdigit():
                    prev += s
                    node = node.next
                    continue
                if prev:
                    if s == "m":
                        alt = int(prev)
                        if alt >= 150 and alt <= 3776:
                            nodes.append(prev + "メートル")
                        else:
                            nodes.append(prev + s)
                    else:
                        nodes.append(prev)
                        nodes.append(s)
                    prev = ""
                    node = node.next
                    continue
                else:
                    nodes.append(s)
                    node = node.next

            replaced_line = [
                self.translation_table.get(node.lower(), node) for node in nodes if node
            ]
            self.logger.warning(f"chunk replaced = {replaced_line}")
            translation_result.append("".join(replaced_line))
        result = "\n ".join(translation_result)
        self.logger.warning(f"translation result = {content} ->\n{result}")
        return result

    def remove_urls_from_chunk(self, chunk: str) -> str:
        url_pattern = re.compile(r"https?:[^\s()]+")
        combined = self.chunk_buffer + re.sub(r"（|）", " ", chunk)
        matches = list(url_pattern.finditer(combined))
        if matches:
            cleaned_chunk = url_pattern.sub(r"", combined)
            removed = 0
            for m in matches:
                start, end = m.span()
                if start > len(self.chunk_buffer):
                    break
                if end > len(self.chunk_buffer):
                    removed += len(self.chunk_buffer) - start
                else:
                    removed += end - start
            cleaned_chunk = cleaned_chunk[len(self.chunk_buffer) - removed :]
            self.chunk_buffer = chunk
            return cleaned_chunk
        else:
            self.chunk_buffer = ""
            return chunk
