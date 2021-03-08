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
</style># Mutable partial

This is analogous to `functools.partial`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

####Examples

Make sure you have run the [setup code](setup.md).

```python
def foo(*args, **kwargs):
    print('args', args)
    print('kwargs', kwargs)
    return 0

model = MyModel()
model.mutable = partial(foo, 'hello world', goodbye='moon')
model.mutable()
```

Out:

```
args ('hello world',)
kwargs {'goodbye': 'moon'}
0
```

##sqlalchemy_mutable.**partial**

<p class="func-header">
    <i>class</i> sqlalchemy_mutable.<b>partial</b>(<i>func, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutable/blob/master/sqlalchemy_mutable/mutable_partial.py#L32">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>__call__</b>(<i>self, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutable/blob/master/sqlalchemy_mutable/mutable_partial.py#L42">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>register</b>(<i>cls, func</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/sqlalchemy-mutable/blob/master/sqlalchemy_mutable/mutable_partial.py#L65">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

