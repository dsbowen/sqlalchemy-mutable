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
</style># Storing models

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##sqlalchemy_mutable.model_shell.**Query**

<p class="func-header">
    <i>class</i> sqlalchemy_mutable.model_shell.<b>Query</b>(<i>scoped_session</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutable/blob/master/sqlalchemy_mutable/model_shell.py#L9">[source]</a>
</p>

Query attribute in database model. Models which have a `query` attribute
will be unshelled automatically when stored and recovered in a `Mutable`
object. See the [setup code](setup.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>scoped_session : <i>sqlalchemy.orm.scoping.scoped_session</i></b>
<p class="attr">
    Current scoped session.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>scoped_session : <i>sqlalchemy.orm.scoping.scoped_session</i></b>
<p class="attr">
    Set from the <code>scoped_session</code> parameter.
</p></td>
</tr>
    </tbody>
</table>





##sqlalchemy_mutable.model_shell.**ModelShell**

<p class="func-header">
    <i>class</i> sqlalchemy_mutable.model_shell.<b>ModelShell</b>(<i>model</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutable/blob/master/sqlalchemy_mutable/model_shell.py#L33">[source]</a>
</p>

The `ModelShell` stores (shells) and recovers (unshells) database
models in `Mutable` objects and `MutableType` columns.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>model : <i>sqlalchemy.ext.declarative.api.Base</i></b>
<p class="attr">
    Database model to store.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>id : <i>usually int or str</i></b>
<p class="attr">
    Identity of the model.
</p>
<b>model_class : <i>class</i></b>
<p class="attr">
    Class of the stored model.
</p></td>
</tr>
    </tbody>
</table>

####Notes

1. The model must have an identity before it is shelled. i.e you must add
it to the session and commit or flush it.
2. Models are unshelled to make comparisons the `__eq__` comparison.

####Examples

Make sure you have run the [setup code](setup.md).

```python
from sqlalchemy_mutable.model_shell import ModelShell

model = MyModel()
session.add(model)
session.commit()
shell = ModelShell(model)
shell.unshell()
```

Out:

```
<__main__.MyModel at 0x7f6bd9936c50>
```

####Methods



<p class="func-header">
    <i></i> <b>unshell</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutable/blob/master/sqlalchemy_mutable/model_shell.py#L99">[source]</a>
</p>

Recover (unshell) a model.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>model or (model_class, id) : <i></i></b>
<p class="attr">
    If the original model has a <code>query</code> attribute, the orginal model is returned. Otherwise, a <code>(model_class, id)</code> tuple is returned which you can use to query the database to recover the model.
</p></td>
</tr>
    </tbody>
</table>

