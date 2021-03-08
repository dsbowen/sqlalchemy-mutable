from docstr_md.python import PySoup, compile_md
from docstr_md.src_href import Github

src_href = Github('https://github.com/dsbowen/sqlalchemy-mutable/blob/master')

path = 'sqlalchemy_mutable/mutable.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
soup.rm_properties()
mutable = [
    obj for obj in soup.objects 
    if hasattr(obj, 'name') and obj.name == 'Mutable'
][0]
mutable.methods = [m for m in mutable.methods if m.name != 'coerce']
soup.import_path = 'sqlalchemy_mutable'
compile_md(soup, compiler='sklearn', outfile='docs_md/basic.md')

path = 'sqlalchemy_mutable/coerced_types.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
soup.objects = soup.objects[0:1]
compile_md(soup, compiler='sklearn', outfile='docs_md/coerced_types.md')

path = 'sqlalchemy_mutable/model_shell.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
compile_md(soup, compiler='sklearn', outfile='docs_md/model_shell.md')

path = 'sqlalchemy_mutable/mutable_list.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
for obj in soup.objects:
    if hasattr(obj, 'name'):
        if obj.name == 'MutableListType':
            obj.methods.clear()
        if obj.name == 'MutableList':
            obj.methods = [m for m in obj.methods if m.name == 'unshell']
soup.import_path = 'sqlalchemy_mutable'
compile_md(soup, compiler='sklearn', outfile='docs_md/mutable_list.md')

path = 'sqlalchemy_mutable/mutable_dict.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
for obj in soup.objects:
    if hasattr(obj, 'name'):
        if obj.name == 'MutableDictType':
            obj.methods.clear()
        if obj.name == 'MutableDict':
            obj.methods = [m for m in obj.methods if m.name == 'unshell']
soup.import_path = 'sqlalchemy_mutable'
compile_md(soup, compiler='sklearn', outfile='docs_md/mutable_dict.md')

path = 'sqlalchemy_mutable/mutable_tuple.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
soup.import_path = 'sqlalchemy_mutable'
compile_md(soup, compiler='sklearn', outfile='docs_md/mutable_tuple.md')

path = 'sqlalchemy_mutable/mutable_partial.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
soup.import_path = 'sqlalchemy_mutable'
compile_md(soup, compiler='sklearn', outfile='docs_md/mutable_partial.md')