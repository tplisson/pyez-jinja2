# pyez-jinja2
Junos PyEZ with Jinja2 templating

## 1. Quick Overview of Jinja2 Templating using the Python interpreter
This is just a short demo to quickly show how Jinja2 templates work with Python

---
### 1.1 Start a Docker container for the PyEZ environment
Using a Docker container greatly simplifies the environment setup for Python, PyEz and Ansible... It also keeps things clean and contained

```
docker run -it --rm -v ~/tom/:/project --name pyez-ansible juniper/pyez-ansible ash
```
See Docker Hub for more info
https://hub.docker.com/r/juniper/pyez-ansible/

### 1.2 Start the Python interpreter
```
python
```

### 1.3 Getting the jinja2 module
Import the "Template" method from the jinja2 module
```
from jinja2 import Template 
```

### 1.4 Instanciating Template()
Create an instance of Template with my interface address variables.
Jinja2 identifies the variables by using double curly brackets.

For example, if I want to configure a number of interfaces on a Junos device with an IPv4 address, I can use the following syntax with 3 variables: the IFD (physical interface name), the unit and an IP address:
```
template = Template('set interface {{ ifd }} unit {{ unit }} family inet address {{ ip }}')
```

### 1.5 Using render()
The template object provides a method called render() which, when called with a dict or keyword arguments, expands the template 

Now I can "expand" the variables with some values:
```
template.render(ifd='ge-0/0/0',unit='101',ip='10.0.1.1/24’)
```
And I can repeat that many times with different values:
```
template.render(ifd='ge-0/0/0',unit='102',ip='10.0.2.1/24’)
```

### 1.6 Stop the Python interpreter
Use Ctrl-D or:
```
exit()
```

## 2. Simple Jinja2 Template in a Python script
Now instead of using the Python interpreter I can write a script that does the same thing. 

### 2.1 Writing a simple Python script
Write a script called "ifa-set.py" that includes the same jinja2 template.
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

### 2.2 Setting file permissions
Make sure the access permissions are properly set to execute this script
```
chmod +x ifa-set.py
```

### 2.3 Running the Python script
Now you're ready to call that script:
```
./ifa-set.py
```
or
```
python ifa-set.py
```

Done.

## 3. Jinja2 Script reading a YAML file
Writing variables within the script means you need to update the script for every variable change. 
Instead you can store the variables in a separate file written in YAML format which is easy to read/update and much cleaner.
It's also a good idea to write your jinja2 template in a separate file while we're at it.

### 3.1 Jinja2 Template file
Write a jinja2 template called "iftemplate.j2":

In 'set commands' format:
```
set interfaces {{ ifd }} unit {{ unit }} family int address {{ ip }}
```

Or in 'curly bracket' style:
```
interfaces {
    {{ ifd }} {
        unit {{ ifd.unit }} {
            family inet {
                address {{ ifd.ip }};
            }
        }
    }
}
```

### 3.2 YAML file for Variables
Store the variables in a YAML file called "ifvars.yml":
```
---
ifd:
  ge-0/0/1:
    unit: 0
    ip: 10.0.1.1/24
  ge-0/0/2:
    unit: 0
    ip: 10.0.2.1/24
  ge-0/0/3:
    unit: 0
    ip: 10.0.3.1/24
  ge-0/0/4:
    unit: 0
    ip: 10.0.4.1/24
  ge-0/0/5:
    unit: 0
    ip: 10.0.5.1/24
```
### 2.1 Writing a simple Python script
Write a script called "ifa-set.py" that includes the same jinja2 template.
We then expand the variables with render() method for two logical interfaces and print the results.
```
#!/usr/bin/python


