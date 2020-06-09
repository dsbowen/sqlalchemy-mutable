<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

<link rel="stylesheet" href="https://assets.readthedocs.org/static/css/readthedocs-doc-embed.css" type="text/css" />

<style>
    a.src-href {
        float: right;
    }
    p.attr {
        margin-top: 0.5em;
        margin-left: 1em;
    }
    p.func-header {
        background-color: gainsboro;
        border-radius: 0.1em;
        padding: 0.5em;
        padding-left: 1em;
    }
    table.field-table {
        border-radius: 0.1em
    }
</style># Basic objects

The basic objects of SQLAlchemy-Mutable are:

1. `MutableModelBase`. Base class for database models with `MutableType`
columns.
2. `MutableType`. Column type associated with `Mutable` objects.
3. `Mutable`. Generic mutable object which automatically tracks changes to its
attributes and items.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##sqlalchemy_mutable.**MutableModelBase**



Base class for database models with `MutableType` columns. This allows you to store and retrieve database models in `MutableType` columns.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

####Examples

Make sure you have run the [setup code](setup.md).

```python
model0 = MyModel()
model1 = MyModel()
session.add_all([model0, model1])
session.commit()
model0.mutable = model1
# without subclassing `MutableModelBase`,
# this would not retrieve `model1`
model0.mutable
```

Out:

```
<__main__.MyModel at 0x7f6bd9936668>
```



##sqlalchemy_mutable.**MutableType**



Column type associated with `Mutable` objects. `MutableType` database columns may be set to:

1. Coerced types. SQLAlchemy-Mutable automatically coerces common objects
such as `int`, `str`, and `datetime`.
2. `Mutable` objects. SQLAlchemy-Mutable automatically converts `list` and
`dict` to mutable objects.
3. Database models.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





##sqlalchemy_mutable.**Mutable**



Base class for mutable objects. Mutable objects track changes to their
'children' (their attributes and items).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>root : <i>sqlalchemy_mutable.Mutable</i></b>
<p class="attr">
    Root mutable object.
</p></td>
</tr>
    </tbody>
</table>

####Examples

Make sure you have run the [setup code](setup.md).

```python
model = MyModel()
session.add(model)
model.mutable.nested_mutable = Mutable()
session.commit()
# if `MyModel.mutable` weren't a `MutableType` column,
# this change would not survive a commit
model.mutable.nested_mutable.greeting = 'hello world'
session.commit()
model.mutable.nested_mutable.greeting
```

Out:

```
'hello, world!'
```

####Methods



<p class="func-header">
    <i></i> <b>register_coerced_type</b>(<i>cls, origin_type</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutable/sqlalchemy_mutable/mutable.py#L116">[source]</a>
</p>

Decorator for coerced type registration.

When a `MutableType` column is set to an object of the origin type
(i.e. when the `coerce` method is invoked), the object is first
converted to a coerced type.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>origin_type : <i>class</i></b>
<p class="attr">
    The origin class.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>register : <i>callable</i></b>
<p class="attr">
    Function to register an origin type.
</p></td>
</tr>
    </tbody>
</table>

####Notes

This does not affect tracked items and attributes. That is, objects of
origin types will not be coerced with the `_convert` method is invoked.

####Examples

Make sure you have run the [setup code](setup.md).

```python
class MyClass():
    def greet(self, name='world'):
        return 'hello, {}!'.format(name)

@Mutable.register_coerced_type(MyClass)
class CoercedMyClass(Mutable, MyClass):
    pass

model = MyModel()
# without registering an associated coerced type,
# this will throw an error
model.mutable = MyClass()
model.mutable.greet()
```

Out:

```
'hello, world!'
```



<p class="func-header">
    <i></i> <b>register_tracked_type</b>(<i>cls, origin_type</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutable/sqlalchemy_mutable/mutable.py#L171">[source]</a>
</p>

Decorator for tracked type registration.

The origin_type maps to a tracked_type. Objects of origin types will be converted to objects of tracked types when the convert method is invoked. Conversion occurs automatically on coersion and when
setting attributes and items.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>origin_type : <i>class</i></b>
<p class="attr">
    The origin class.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>register : <i>callable</i></b>
<p class="attr">
    Function to register an origin type.
</p></td>
</tr>
    </tbody>
</table>

####Examples

Make sure you have run the [setup code](setup.md).

```python
class MyClass():
    def __init__(self, name):
        self.name = name

    def greet(self):
        return 'hello, {}!'.format(self.name)

@Mutable.register_tracked_type(MyClass)
class MutableMyClass(MyClass, Mutable):
    def __init__(self, source=None, root=None):
        '''
        Parameters
        ----------
        source : MyClass
            Original instance of `MyClass`. This will be converted
            into a `MutableMyClass` object.

        root : Mutable or None, default=None
            Root mutable object. This is handled by
            SQLAlchemy-Mutable. Set to `None` by default.
        '''
        super().__init__(name=source.name)

model = MyModel()
session.add(model)
model.mutable = Mutable()
model.mutable.object = MyClass('world')
session.commit()
# without registering MyClass as a tracked type,
# this change would not survive a commit
model.mutable.object.name = 'moon'
session.commit()
model.mutable.object.greet()
```

Out:

```
'hello, moon!'
```



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

