from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'This is my homepage'

# One underscore
#   - _ name points to the result of the last executed statement in an interactive interpreter session
#   - _ is used as a throw-away name.
#   - _ being used as a function (import ugettext as _)

# Double underscore at the beginning
#   - Python mangles these names and it is used to avoid name clashes with names defined by subclasses
'''
class A(object):
...     def _internal_use(self):
...         pass
...     def __method_name(self):
...         pass
... 
>>> dir(A())
['_A__method_name', ..., '_internal_use']
'''

# Double Underscore Before and After a Name
#   - These are special method names used by Python.
#   - __new__(), __init__(), __del__(), __repr__()

#   - Before executing the code, it will define a few special variables.
#   - if the python interpreter is running that module (the source file) as the main program,
#       it sets the special __name__ variable to have a value "__main__". If this file is
#       being imported from another module, __name__ will be set to the module's name.

if __name__ == "__main__":
    app.run('0.0.0.0')