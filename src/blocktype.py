from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

    def block_to_block_type(block):
        if re.match(r"#{1,6} ", block):
            return BlockType.HEADING
        
        if re.fullmatch(r"```.*```", block, re.DOTALL):
            return BlockType.CODE
        
        if re.match(r"> ", block):
            lines = block.split("\n")
            for line in lines:
                if not re.match(r">", line):
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE
        
        if re.match(r"- ", block):
            lines = block.split("\n")
            for line in lines:
                if not re.match(r"- ", line):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        
        if re.match(r"1\. ", block):
            i = 1
            lines = block.split("\n")
            for line in lines:
                if not re.match(f"{i}. ", line):
                    return BlockType.PARAGRAPH
                i += 1
            return BlockType.ORDERED_LIST
        
        return BlockType.PARAGRAPH



        
