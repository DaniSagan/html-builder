# -*- coding=utf-8 -*-

from __future__ import print_function
import os, subprocess

class Attribute(object):
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def __str__(self):
        return '%s="%s"' % (self.name, self.data)


class Element(object):
    def __init__(self, tag=None, attributes=None):
        self.tag = tag
        if attributes:
            self.attributes = attributes
        else:
            self.attributes = []
        self.data = []

    def _start_tag_str(self, indent_level=0):
        result = ''
        result += '<%s' % self.tag
        if self.attributes:
            result += ' '
            result += ' '.join(map(str, self.attributes))
        result += '>'
        return result

    def _end_tag_str(self):
        result = '</%s>' % self.tag
        return result

    def add_element(self, element):
        self.data.append(element)
        return element

    def to_string(self, indent_level=0):
        result = ''
        result += '\t'*indent_level + self._start_tag_str() + '\n'
        for d in self.data:
            result += d.to_string(indent_level+1) + '\n'
        result += '\t'*indent_level + self._end_tag_str()
        return result

class VoidElement(Element):
    def __init__(self, tag=None, attributes=None):
        Element.__init__(self, tag, attributes)

    def to_string(self, indent_level=0):
        return '\t'*indent_level + self._start_tag_str()


class RootElement(Element):
    def __init__(self):
        Element.__init__(self)

    def __str__(self):
        return ''.join(map(str, self.data))

    def to_string(self, indent_level=0):
        result = '<!DOCTYPE html>\n'
        for d in self.data:
            result += d.to_string(indent_level) + '\n'
        return result


class TextElement(Element):
    def __init__(self, text):
        Element.__init__(self)
        self.text = text

    def __str__(self):
        return self.text

    def to_string(self, indent_level=0):
        return '\t'*indent_level + self.text


class H1TextElement(Element):
    def __init__(self, text):
        Element.__init__(self, 'h1')
        self.add_element(TextElement(text))


class H2TextElement(Element):
    def __init__(self, text):
        Element.__init__(self, 'h2')
        self.add_element(TextElement(text))

class HeadingLevel(object):
    L1 = 1
    L2 = 2
    L3 = 3
    L4 = 4
    L5 = 5
    L6 = 6


class HeadingTextElement(Element):
    def __init__(self, text, level):
        tag = 'h' + str(level)
        Element.__init__(self, tag)
        self.add_element(TextElement(text))


class ImageElement(VoidElement):
    def __init__(self, src):
        VoidElement.__init__(self)
        self.tag = 'img'
        self.attributes.append(Attribute('src', src))

class LinkElement(Element):
    def __init__(self, href, text=None):
        Element.__init__(self)
        self.tag = 'a'
        self.attributes.append(Attribute('href', href))
        if text:
            self.data.append(TextElement(text))
        else:
            self.data.append(TextElement(href))


class DivElement(Element):
    def __init__(self):
        Element.__init__(self, 'div')


class LineBreakElement(VoidElement):
    def __init__(self):
        VoidElement.__init__(self, 'br')


class ListType(object):
    UNORDERED = 0
    ORDERED = 1


class ListItemElement(Element):
    def __init__(self):
        Element.__init__(self, 'li')


class ListContainerElement(Element):
    def __init__(self, list_type):
        if list_type == ListType.UNORDERED:
            tag = 'ul'
        else:
            tag = 'ol'
        Element.__init__(self, tag)

    def add_line(self, line):
        item = self.add_element(ListItemElement())
        item.add_element(TextElement(line))

    def add_lines(self, lines):
        for line in lines:
            self.add_line(line)


class Page(RootElement):
    def __init__(self):
        RootElement.__init__(self)
        self.html = self.add_element(Element('html'))
        self.head = self.html.add_element(Element('head'))
        self.title_element = self.head.add_element(Element('title'))
        self.title = self.title_element.add_element(TextElement('Hello World!'))
        self.body = self.html.add_element(Element('body'))

    def set_title(self, title):
        self.title.text = title

    def save(self, filename):
        with open(filename, 'w') as fobj:
            fobj.write(self.to_string())

    def show(self):
        if(not os.path.exists('.temp')):
            os.makedirs('.temp')
        filename = '.temp/index.html'
        self.save(filename)
        subprocess.call(['gnome-open', filename])
