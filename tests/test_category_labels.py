import unittest
from amazon_android.vision import _canonical_text, _join_wrapped_categories


class CategoryLabelsTests(unittest.TestCase):
    def test_wrapped_category_titles_in_user_images_are_joined(self):
        for first, second, expected in [('Groceries and','Drinks','Groceries and Drinks'),
                                         ('Home and','DIY','Home and DIY'),
                                         ('Books and','Reading','Books and Reading'),
                                         ('Deals &','Savings','Deals & Savings'),
                                         ('Be Inspired,','Save More','Be Inspired, Save More'),
                                         ('Health and','Personal Care','Health and Personal Care'),
                                         ('Devices and','Electronics','Devices and Electronics'),
                                         ('Music, Video','and Gaming','Music, Video and Gaming'),
                                         ('Toys, Kids and','Baby','Toys, Kids and Baby'),
                                         ('Office &','Professional','Office & Professional'),
                                         ('Sports &','Outdoors','Sports & Outdoors')]:
            parts=[{'text':first,'raw':first,'box':(20,100,120,115),'score':.99,'index':0},
                   {'text':second,'raw':second,'box':(20,119,90,134),'score':.98,'index':1}]
            merged=_join_wrapped_categories(parts)
            self.assertEqual(merged[-1]['text'],expected)
            self.assertEqual(merged[-1]['box'],(20,100,120,134))

    def test_incomplete_title_is_not_fuzzily_promoted_to_full_category(self):
        for first in ('Home and', 'Toys, Kids and', 'Be Inspired,'):
            self.assertEqual(_canonical_text(first), first)

    def test_text_in_another_card_cannot_be_joined(self):
        parts=[{'text':'Home and','raw':'Home and','box':(20,100,100,115),'score':.99,'index':0},
               {'text':'DIY','raw':'DIY','box':(170,119,220,134),'score':.99,'index':1}]
        self.assertEqual(len(_join_wrapped_categories(parts)),2)

    def test_small_overlap_between_ocr_lines_does_not_lose_books_title(self):
        parts=[{'text':'Books and','raw':'Books and','box':(20,100,100,116),'score':.99,'index':0},
               {'text':'Reading','raw':'Reading','box':(19,115,95,134),'score':.99,'index':1}]
        self.assertEqual(_join_wrapped_categories(parts)[-1]['text'],'Books and Reading')


if __name__=='__main__':
    unittest.main()
