#!/usr/bin/python

import yaml
from jinja2 import Template

mytemplate = "conf.j2"
myinput = "ifvars.yml"

### Print the Jinja2 Template file
myj2 = open(mytemplate).read()
#print "\n### DEBUG: Print the Jinja2 template:"
#print myj2

### Print the YAML input file
mydata = yaml.load(open(myinput).read())
#print "\n### DEBUG: Print the YAML file:"
#print mydata

### Render the jinja2 template
mytemplate = Template(myj2)
myconfig = mytemplate.render(mydata)
print "\n### Here's the full config:"
print myconfig