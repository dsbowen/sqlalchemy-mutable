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
</style># Mutable dictionary

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

####Examples

Make sure you have run the [setup code](setup.md).

```python
model = MyModel()
model.mutable = {}
session.add(model)
session.commit()
# without a mutable dictionary,
# this change will not survive a commit
model.mutable['hello'] = 'world'
session.commit()
model.mutable
```

Out:

```
{'hello': 'world'}
```

##sqlalchemy_mutable.**MutableDictType**



Mutable dictionary database type.

In the setup code, we use a `MutableType` database column, which handles
dictionaries as well as other objects. To force the column to be a
dictionary, substitute `MutableDictType` for `MutableType`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





##sqlalchemy_mutable.**MutableDict**

<p class="func-header">
    <i>class</i> sqlalchemy_mutable.<b>MutableDict</b>(<i>source={}, root=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutable/blob/master/sqlalchemy_mutable/mutable_dict.py#L51">[source]</a>
</p>

Subclasses `dict`, and implements all `dict` methods.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>source : <i>dict, default={}</i></b>
<p class="attr">
    Source object which will be converted into a mutable dictionary.
</p>
<b>root : <i>sqlalchemy_mutable.Mutable or None, default=None</i></b>
<p class="attr">
    Root mutable object. If <code>None</code>, <code>self</code> is assumed to be the root.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>unshell</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutable/blob/master/sqlalchemy_mutable/mutable_dict.py#L123">[source]</a>
</p>

Call to force values to unshell. Normally this occurs automatically.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>copy : <i>dict</i></b>
<p class="attr">
    Shallow copy of <code>self</code> where all <code>ModelShell</code> values are unshelled.
</p></td>
</tr>
    </tbody>
</table>





<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

