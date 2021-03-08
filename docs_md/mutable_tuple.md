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
</style># Mutable tuple

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

####Notes

In the setup code, we use a `MutableType` database column that handles tuples
as well as other objects. To force the column to be a tuple, substitute `MutableTupleType` or `MutableTupleJSONType` for `MutableType`.

####Examples

Make sure you have run the [setup code](setup.md).

```python
model0 = MyModel()
model1 = MyModel()
model0.mutable = [(model1,)]
session.add_all([model0, model1])
session.commit()
# without a mutable tuple,
# this change would not appear after a commit
model1.greeting = 'hello world'
session.commit()
model0.mutable[0][0].greeting
```

Out:

```
'hello world'
```

##sqlalchemy_mutable.**MutableTupleType**



Mutable tuple database type with pickle serialization.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





##sqlalchemy_mutable.**MutableTupleJSONType**



Mutable tuple database type with JSON serialization.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





##sqlalchemy_mutable.**MutableTuple**





<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>source : <i>tuple, default=()</i></b>
<p class="attr">
    Source objects that will be converted into a mutable tuple.
</p>
<b>root : <i>sqlalchemy.Mutable or None, default=None</i></b>
<p class="attr">
    Root mutable object. If <code>None</code>, <code>self</code> is assumed to be the root.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>coerce</b>(<i>cls, key, obj</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutable/blob/master/sqlalchemy_mutable/mutable_tuple.py#L64">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>unshell</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutable/blob/master/sqlalchemy_mutable/mutable_tuple.py#L91">[source]</a>
</p>

Call to force values to unshell. Normally, this occurs automatically.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>copy : <i>tuple</i></b>
<p class="attr">
    Shallow copy of <code>self</code> where all <code>ModelShell</code> items are unshelled.
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





<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

