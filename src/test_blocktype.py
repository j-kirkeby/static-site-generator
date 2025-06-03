import unittest

from blocktype import BlockType


class TestBlockType(unittest.TestCase):
    def test_blocktype_heading(self):
        # Finds correct headings
        block_h1 = "# Heading1"
        self.assertEqual(BlockType.HEADING, BlockType.block_to_block_type(block_h1))
        block_h2 = "## Heading2"
        self.assertEqual(BlockType.HEADING, BlockType.block_to_block_type(block_h2))
        block_h3 = "### Heading3"
        self.assertEqual(BlockType.HEADING, BlockType.block_to_block_type(block_h3))
        block_h4 = "#### Heading4"
        self.assertEqual(BlockType.HEADING, BlockType.block_to_block_type(block_h4))
        block_h5 = "##### Heading5"
        self.assertEqual(BlockType.HEADING, BlockType.block_to_block_type(block_h5))
        block_h6 = "###### Heading6"
        self.assertEqual(BlockType.HEADING, BlockType.block_to_block_type(block_h6))
        
        # Does not recognize incorrect headings
        block_no_space = "#Heading"
        self.assertNotEqual(BlockType.HEADING, BlockType.block_to_block_type(block_no_space))
        block_h7 = "####### Heading 7"
        self.assertNotEqual(BlockType.HEADING, BlockType.block_to_block_type(block_h7))

    def test_blocktype_code(self):
        # Finds correct code blocks
        code_block = "```code goes here\n more code `inline code````"
        self.assertEqual(BlockType.CODE, BlockType.block_to_block_type(code_block))

        # Does not recognize incorrect code blocks
        not_code = "letters ```is this a block``` haha"
        self.assertNotEqual(BlockType.CODE, BlockType.block_to_block_type(not_code))
    
    def test_blocktype_quote(self):
        # Finds correct quote blocks
        quote_block = """
> This is a quote
> More quote
> Even more quote
"""
        quote_block = quote_block.strip()
        self.assertEqual(BlockType.QUOTE, BlockType.block_to_block_type(quote_block))
        
        # Does not recognize incorrect quote blocks
        quote_block = """
> This is a quote
> More quote
Haha actually not a quote block
"""
        quote_block = quote_block.strip()
        self.assertNotEqual(BlockType.QUOTE, BlockType.block_to_block_type(quote_block))

    def test_blocktype_unorlist(self):
        # Finds correct unordered lists
        list_block = """
- list
- list item 2
- list item 3
"""
        list_block = list_block.strip()
        self.assertEqual(BlockType.UNORDERED_LIST, BlockType.block_to_block_type(list_block))

        # Does not recognize incorrect lists
        list_block = """
- list
 - list item 2
- list item 3
"""
        list_block = list_block.strip()
        self.assertNotEqual(BlockType.UNORDERED_LIST, BlockType.block_to_block_type(list_block))

        list_block = """
- list
- list item 2
-list item 3
"""
        list_block = list_block.strip()
        self.assertNotEqual(BlockType.UNORDERED_LIST, BlockType.block_to_block_type(list_block))

        list_block = """
- list
- list item 2
list item 3
"""
        list_block = list_block.strip()
        self.assertNotEqual(BlockType.UNORDERED_LIST, BlockType.block_to_block_type(list_block))

    def test_blocktype_orlist(self):
        # Finds correct unordered lists
        list_block = """
1. list
2. list item 2
3. list item 3
"""
        list_block = list_block.strip()
        self.assertEqual(BlockType.ORDERED_LIST, BlockType.block_to_block_type(list_block))

        # Does not recognize incorrect lists
        list_block = """
1. list
 2. list item 2
3. list item 3
"""
        list_block = list_block.strip()
        self.assertNotEqual(BlockType.ORDERED_LIST, BlockType.block_to_block_type(list_block))

        list_block = """
1. list
3. list item 2
2. list item 3
"""
        list_block = list_block.strip()
        self.assertNotEqual(BlockType.ORDERED_LIST, BlockType.block_to_block_type(list_block))

        list_block = """
1. list
2.list item 2
3. list item 3
"""
        list_block = list_block.strip()
        self.assertNotEqual(BlockType.ORDERED_LIST, BlockType.block_to_block_type(list_block))


if __name__ == "__main__":
    unittest.main()