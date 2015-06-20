#! /usr/bin/python
# -*- coding=utf-8 -*-

from __future__ import print_function
from htmlbuilder import *

if __name__ == '__main__':
    page = Page()

    # header
    page.set_title("Webpage automatically generated")

    # navigation
    div_navigation = DivElement()

    # body content
    page.body.add_element(HeadingTextElement('This is the Title!!', HeadingLevel.L1))
    page.body.add_element(HeadingTextElement('This is a subtitle', HeadingLevel.L2))

    img_source = 'https://www.python.org/static/community_logos/python-logo-master-v3-TM.png'
    page.body.add_element(ImageElement(img_source))
    page.body.add_element(LineBreakElement())

    page.body.add_element(TextElement('This is a link: '))
    page.body.add_element(LinkElement('http://www.google.com'))
    page.body.add_element(LineBreakElement())

    page.body.add_element(TextElement('This is an ordered list:'))
    olist = page.body.add_element(ListContainerElement(ListType.ORDERED))
    olist.add_lines(['ordered list item %d' % k for k in range(1, 11)])

    page.body.add_element(TextElement('This is an unordered list:'))
    ulist = page.body.add_element(ListContainerElement(ListType.UNORDERED))
    ulist.add_lines(['unordered list item %d' % k for k in range(1, 11)])

    page.show()
