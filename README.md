# Junos PyEZ with Jinja2 templating

[![Build Status](https://travis-ci.org/tplisson/pyez-jinja2.svg?branch=master)](https://travis-ci.org/tplisson/pyez-jinja2)

## Table of Contents

[**1. Quick Jinja2 Demo using the Python Interpreter**](README.md#1.-Quick-Jinja2-Demo-using-the-python-interpreter)

[**2. Simple Python script with a Jinja2 Template**](README.md#2.-Simple-Python-script-with-a-Jinja2-Template)

[**3. Python Script with Jinja2 using YAML files**](README.md#3.-Python-Script-with-Jinja2-using-YAML-files)


# 1. Quick Jinja2 Demo using the Python Interpreter
This is just a short demo to quickly show how Jinja2 templates work with Python

---
## 1.1 Start a Docker container for the PyEZ environment
Using a Docker container greatly simplifies the environment setup for Python, PyEz and Ansible... It also keeps things clean and contained

```
docker run -it --rm -v $(pwd):/project --name pyez-ansible juniper/pyez-ansible ash
```
See Docker Hub for more info
https://hub.docker.com/r/juniper/pyez-ansible/

## 1.2 Start the Python interpreter
```
python
```

## 1.3 Getting the jinja2 module
Import the "Template" method from the jinja2 module
```
from jinja2 import Template 
```

## 1.4 Instanciating Template()
Create an instance of Template with my interface address variables.
Jinja2 identifies the variables by using double curly brackets.

For example, if I want to configure a number of interfaces on a Junos device with an IPv4 address, I can use the following syntax with 3 variables: the IFD (physical interface name), the unit and an IP address:
```
template = Template('set interface {{ ifd }} unit {{ unit }} family inet address {{ ip }}')
```

## 1.5 Using render()
The template object provides a method called render() which, when called with a dict or keyword arguments, expands the template 

Now you can "expand" the variables with some values:
```
template.render(ifd='ge-0/0/0',unit='101',ip='10.0.1.1/24’)
```
And you can repeat that many times with different values:
```
template.render(ifd='ge-0/0/0',unit='102',ip='10.0.2.1/24’)
```

## 1.6 Stop the Python interpreter
Use Ctrl-D or:
```
exit()
```

# 2. Simple Python script with a Jinja2 Template
Now instead of using the Python interpreter I can write a script that does the same thing. 

## 2.1 Writing a simple Python script
Write a script called "genconfig.py" that includes the same jinja2 template.
We then expand the variables with render() method for two logical interfaces and print the results.
```
#!/usr/bin/python

from jinja2 import Template
template = Template('set interface {{ ifd }} unit {{ unit }} family inet address {{ ip }}')
ifa1 = template.render(ifd='ge-0/0/0',unit='101',ip='10.0.1.1/24')
print ifa1
ifa2 = template.render(ifd='ge-0/0/0',unit='102',ip='10.0.2.1/24')
print ifa2
```

## 2.2 Setting file permissions
Make sure the access permissions are properly set to execute this script
```
chmod +x genconfig.py
```

## 2.3 Running the Python script
Now you're ready to call that script:
```
./genconfig.py
```
or
```
python genconfig.py
```

Done.


# 3. Python Script with Jinja2 using YAML files
Writing variables within the script means you need to update the script for every variable change. 
Instead you can store the variables in a separate file written in YAML format which is easy to read/update and much cleaner.
It's also a good idea to write your jinja2 template in a separate file while we're at it.

## 3.1 Jinja2 Template file
Write a jinja2 template called "conf.j2":

In 'set commands' format:
```
{% for item in ifd %}
set interfaces {{ item.name }} unit {{ item.unit }} family int address {{ item.ip }}
{% endfor %}
```

Or in 'curly bracket' style:
```
interfaces {
{% for item in ifd %}
    {{ item.name }} {
        unit {{ item.unit }} {
            family inet {
                address {{ item.ip }};
            }
        }
    }
{% endfor %}
}
```

## 3.2 YAML file for Variables
Store the variables in a YAML file called "ifvars.yml":
```
---
ifd:
- name: 'ge-0/0/1'
  unit: 0
  ip: 10.0.1.1/24
- name: ge-0/0/2 
  unit: 0
  ip: 10.0.2.1/24
- name: ge-0/0/3
  unit: 0
  ip: 10.0.3.1/24 
- name: ge-0/0/4
  unit: 0
  ip: 10.0.4.1/24
- name: ge-0/0/5
  unit: 0
  ip: 10.0.5.1/24
```

## 3.3 Writing a simple Python script
Write a script called "genconfig.py" that includes the same jinja2 template.
We then expand the variables with render() method for two logical interfaces and print the results.
```
#!/usr/bin/python

import yaml
from jinja2 import Template

mytemplate = "setconf.j2"
myinput = "ifd.yml"

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
```

## 3.4 Setting file permissions
Make sure the access permissions are properly set to execute this script
```
chmod +x genconfig.py
```

## 3.5 Running the Python script
Now you're ready to call that script:
```
./genconfig.py
```
or
```
python genconfig.py
```

Done.
