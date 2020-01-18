# SQLAlchemy-Mutable

SQLAlchemy-Mutable provides generic nested mutable objects and iterables for [SQLAlchemy](https://www.sqlalchemy.org). Its primary features are:

1. Nested mutation tracking
2. Mutation tracking for iterables (```list``` and ```dict```)
3. Support for embedded database models
4. Support for common literals and `datetime` objects
5. Support for custom Mutable classes
6. Support for converting existing classes to Mutable classes

## Example: Nested mutation tracking with lists and dicts

```python
x = MyModel()
session.add(x)
x.mutable = {'greeting': []}
session.commit()
x.mutable['greeting'].append('hello world')
session.commit()
print(x.mutable['greeting'][0])
```

Outputs:

```
hello world
```

## Documentation

You can find the latest documentation at [https://dsbowen.github.io/sqlalchemy-mutable](https://dsbowen.github.io/sqlalchemy-mutable).

## License

Publications which use this software should include the following citation:

Bowen, D.S. (2019). SQLAlchemy-Mutable \[Computer software\]. [https://dsbowen.github.io/sqlalchemy-mutable](https://dsbowen.github.io/sqlalchemy-mutable).

This project is licensed under the MIT License [LICENSE](https://github.com/dsbowen/sqlalchemy-mutable/blob/master/LICENSE).

## Acknowledgements

Much inspiration drawn from [SQLAlchemy-JSON](https://pypi.org/project/sqlalchemy-json/)