from flask_nav import Nav
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from dominate import tags
from flask_nav.renderers import Renderer

nav = Nav()

class customRenderer(Renderer):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def visit_Link(self, node):
        return tags.a(node.text, href=node.get_url())

    def visit_Navbar(self, node):
        kwargs = {'_class': 'navbar navbar-fixed-side'}
        kwargs.update(self.kwargs)

        cont = tags.nav(**kwargs)
        ul = cont.add(tags.ul())

        for item in node.items:
            ul.add(tags.li(self.visit(item)))

        return cont

    def visit_View(self, node):
        kwargs = {}
        if node.active:
            kwargs['_class'] = 'active'
        return tags.a(node.text,
                      href=node.get_url(),
                      title=node.text,
                      **kwargs)

    def visit_Subgroup(self, node):
        group = tags.ul(_class='subgroup')
        title = tags.span(node.title)

        if node.active:
            title.attributes['class'] = 'active'

        for item in node.items:
            group.add(tags.li(self.visit(item)))

        return tags.div(title, group)

    def visit_Separator(self, node):
        return tags.hr(_class='separator')

    def visit_Text(self, node):
        return tags.span(node.text, _class='nav-label')

nav.register_element('top', Navbar(
    View('Flask-Bootstrap', 'indexBP.indexView'),
    View('Home', 'indexBP.indexView'),
    View('Dav', 'indexBP.davView'),
    Subgroup('Docs',
        Link('Flask-Bootstrap', 'http://pythonhosted.org/Flask-Bootstrap'),
        Link('Flask-AppConfig', 'https://github.com/mbr/flask-appconfig'),
        Link('Flask-Debug', 'https://github.com/mbr/flask-debug'),
        Separator(),
        Text('Bootstrap'),
        Link('Getting started', 'http://getbootstrap.com/getting-started/'),
        Link('CSS', 'http://getbootstrap.com/css/'),
        Link('Components', 'http://getbootstrap.com/components/'),
        Link('Javascript', 'http://getbootstrap.com/javascript/'),
        Link('Customize', 'http://getbootstrap.com/customize/'), ), ))
