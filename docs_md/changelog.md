# Change log

## Version 0.0.13

- Added nested model unshelling
- Removed automatic unshelling on `__iter__` for `MutableList` and `MutableTuple` to improve runtime. To unshell these objects, use their `unshell` method.

Possible TODO:

- Only shell models when mutable objects are being pickled

## Version 0.0.12

- Added support for mutable tuples

## Version 0.0.11

- Fixed bug in `MutableList.sort`

## Version 0.0.9

- Support for setting mutable column types to functions and partial functions
- Support for setting mutable column types to boolean values