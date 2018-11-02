#!/usr/bin/python

from jinja2 import Template
template = Template('set interface {{ ifd }} unit {{ unit }} family inet address {{ ip }}')
ifa1 = template.render(ifd='ge-0/0/0',unit='101',ip='10.0.1.1/24')
print ifa1
ifa2 = template.render(ifd='ge-0/0/0',unit='102',ip='10.0.2.1/24')
print ifa2