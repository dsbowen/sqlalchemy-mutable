# Advanced type conversion

Some types require more work to convert into mutable types. We illustrate advanced use by creating our own mutable list type.

Make sure you have run the [setup code](setup.md).

```python
@Mutable.register_tracked_type(list) 
class MutableList(Mutable, list):
    def __init__(self, source=[], root=None):
        # 1. convert potentially mutable attributes/items to Mutable objects
        converted_list = self._convert_iterable(source)
        super().__init__(converted_list)
    
    # 2. classes with mutable items must have a `_tracked_items` attribute
    # `_tracked_items` is a list of potentially mutable items
    @property
    def _tracked_items(self):
        return list(self)
    
    # 3. call `self._changed()` to register change with the root Mutable object
    def append(self, item):
        self._changed()
        super().append(self._convert_item(item))
        
model = MyModel()
model.mutable = []
session.add(model)
session.commit()
# without using a mutable list, this change would not survive a commit
model.mutable.append('hello world')
session.commit()
model.mutable
```

Out:

```
['hello world']
```