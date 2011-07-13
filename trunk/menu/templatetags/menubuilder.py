from menu.models import Menu, MenuItem
from django import template

register = template.Library()

def recursive_menu(context):
    current_path = context['request'].path
    slug = current_path.split('/')[1]
    menu = Menu.objects.get(slug=slug)
    sub_menus = Menu.objects.filter(parent_menu_id=menu.id).order_by('id')
    menu_items = MenuItem.objects.filter(menu=menu)
    try:
        this_menu_item = MenuItem.objects.get(link_url=current_path)
        this_menu = None
    except:
        try:
            this_menu = Menu.objects.get(base_url=current_path)
        except:
            this_menu = None
        this_menu_item = None


    if current_path.startswith('/bailout'):
        #super mega hack for bailout ordering -- Fix later you bum! (Kaitlin)
        sub_menus_1 = ( Menu.objects.get(id=11),)
        html = get_menu(current_path, slug, menu, sub_menus_1, [], this_menu_item, this_menu)
        html += get_menu_ugly_fdic_exception(current_path, slug, menu, [Menu.objects.get(id=14),], [], this_menu_item, this_menu)
        menu_items_1 = (MenuItem.objects.get(id=86),)
        html += get_menu(current_path, slug, menu, [], menu_items_1, this_menu_item, this_menu)
        sub_menus_2 = (Menu.objects.get(id=16),)
        html += get_menu(current_path, slug, menu, sub_menus_2, [], this_menu_item, this_menu)

    else:
        html = get_menu(current_path, slug, menu, sub_menus, menu_items, this_menu_item, this_menu)

    menu_data = '<ul>' + ''.join(html) + '</ul>'

    if current_path.startswith('/tax_expenditures'):
        return { 'menu_data': menu_data, 'menu_items': menu_items, 'pted':True }
    else:
        return { 'menu_data': menu_data, 'menu_items': menu_items }


def get_menu(current_path, slug, menu, sub_menus, menu_items, this_menu_item, this_menu):
    html = []
    for sm in sub_menus:
        menu_list = []
        current_page = False
        for mi in MenuItem.objects.filter(menu=sm):
            if current_path.startswith(mi.link_url):
                menu_list.append('<li class="active"><a href="' + mi.link_url + '">'+ mi.title + '</a></li>')
                current_page = True
            else:
                menu_list.append('<li><a href="' + mi.link_url + '">'+ mi.title+ '</a></li>')
        
        for lm in Menu.objects.filter(parent_menu_id=sm.id):
            leaf_menu = []
            current_leaf_page = False
            for lm_item in MenuItem.objects.filter(menu=lm):
                if current_path.startswith(lm_item.link_url):
                    leaf_menu.append('<li class="active"><a href="' + lm_item.link_url + '">'+ lm_item.title + '</a></li>')
                    current_leaf_page = True
                else:
                    leaf_menu.append('<li><a href="' + lm_item.link_url + '">'+ lm_item.title + '</a></li>')
            if current_leaf_page or lm.base_url == current_path:
                leaf_menu.insert(0, '<li class="active"><a href="' + lm.base_url + '">' + lm.name + '</a><ul>')
            else:
                leaf_menu.insert(0, '<li><a href="'+ lm.base_url + '">' + lm.name + '</a><ul>')

            leaf_menu.append('</ul></li>')

            menu_list.extend(leaf_menu)
        
        if current_page or \
            current_path.startswith(sm.base_url) or \
            (this_menu_item and this_menu_item.menu and this_menu_item.menu.parent_menu_id == sm.id ) or \
            (this_menu and this_menu.parent_menu_id == sm.id):
            menu_list.insert(0, '<li class="active"><span class="expanded accordion"></span><a href="'+ sm.base_url + '">'+ sm.name +'</a><ul>')
        else:
            menu_list.insert(0, '<li><span class="collapsed accordion"></span><a href="' + sm.base_url + '">' + sm.name + '</a><ul class="collapsed">')
        
        menu_list.append('</ul></li>')
#        menu_data.append(menu_list)
        html.extend(menu_list)
    
    for mi in menu_items:
        if current_path.startswith(mi.link_url):
            html.append('<li class="active"><span class="accordion"></span><a href="'+mi.link_url +'">'+ mi.title + '</a></li>')
        else:
            html.append('<li><span class="accordion"></span><a href="'+mi.link_url +'">'+ mi.title + '</a></li>')

    return ''.join(html)


def get_menu_ugly_fdic_exception(current_path, slug, menu, sub_menus, menu_items, this_menu_item, this_menu):  #omigod destroy this asap
    html = []
    for sm in sub_menus:
        menu_list = []
        current_page = False
        mis = MenuItem.objects.filter(menu=sm)
        if current_path.startswith(mis[0].link_url):
            menu_list.append('<li class="active"><a href="' + mis[0].link_url + '">'+ mis[0].title + '</a></li>')
            current_page = True
        else:
            menu_list.append('<li><a href="' + mis[0].link_url + '">'+ mis[0].title+ '</a></li>')

        for lm in Menu.objects.filter(parent_menu_id=sm.id):
            leaf_menu = []
            current_leaf_page = False
            for lm_item in MenuItem.objects.filter(menu=lm):
                if current_path.startswith(lm_item.link_url):
                    leaf_menu.append('<li class="active"><a href="' + lm_item.link_url + '">'+ lm_item.title + '</a></li>')
                    current_leaf_page = True
                else:
                    leaf_menu.append('<li><a href="' + lm_item.link_url + '">'+ lm_item.title + '</a></li>')
            if current_leaf_page or lm.base_url == current_path:
                leaf_menu.insert(0, '<li class="active"><a href="' + lm.base_url + '">' + lm.name + '</a><ul>')
            else:
                leaf_menu.insert(0, '<li><a href="'+ lm.base_url + '">' + lm.name + '</a><ul>')

            leaf_menu.append('</ul></li>')

            menu_list.extend(leaf_menu)
        

        
        for mi in mis[1:]:
            if current_path.startswith(mi.link_url):
                menu_list.append('<li class="active"><a href="' + mi.link_url + '">'+ mi.title + '</a></li>')
                current_page = True
            else:
                menu_list.append('<li><a href="' + mi.link_url + '">'+ mi.title+ '</a></li>')
 
        if current_page or \
            current_path.startswith(sm.base_url) or \
            (this_menu_item and this_menu_item.menu and this_menu_item.menu.parent_menu_id == sm.id ) or \
            (this_menu and this_menu.parent_menu_id == sm.id):
            menu_list.insert(0, '<li class="active"><span class="expanded accordion"></span><a href="'+ sm.base_url + '">'+ sm.name +'</a><ul>')
        else:
            menu_list.insert(0, '<li><span class="collapsed accordion"></span><a href="' + sm.base_url + '">' + sm.name + '</a><ul class="collapsed">')
       
        menu_list.append('</ul></li>')
#        menu_data.append(menu_list)
        html.extend(menu_list)
    
    for mi in menu_items:
        if current_path.startswith(mi.link_url):
            html.append('<li class="active"><span class="accordion"></span><a href="'+mi.link_url +'">'+ mi.title + '</a></li>')
        else:
            html.append('<li><span class="accordion"></span><a href="'+mi.link_url +'">'+ mi.title + '</a></li>')

    return ''.join(html)


def build_menu(parser, token):
    """
    {% menu menu_name %}
    """
    try:
        tag_name, menu_name = token.split_contents()
    except:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]
    return MenuObject(menu_name)

class MenuObject(template.Node):
    def __init__(self, menu_name):
        self.menu_name = menu_name

    def render(self, context):
        current_path = template.resolve_variable('request.path', context)
        user = template.resolve_variable('request.user', context)
        context['menuitems'] = get_items(self.menu_name, current_path, user)
        return ''

def build_sub_menu(parser, token):
    """
    {% submenu %}
    """
    return SubMenuObject()

class SubMenuObject(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        current_path = template.resolve_variable('request.path', context)
        user = template.resolve_variable('request.user', context)
        menu = False
        for m in Menu.objects.filter(base_url__isnull=False):
            if m.base_url and current_path.startswith(m.base_url):
                menu = m

        if menu:
            context['submenu_items'] = get_items(menu.slug, current_path, user)
            context['submenu'] = menu
        else:
            context['submenu_items'] = context['submenu'] = None
        return ''

def get_items(menu, current_path, user):
    menuitems = []
    for i in MenuItem.objects.filter(menu__slug=menu).order_by('order'):
        current = ( i.link_url != '/' and current_path.startswith(i.link_url)) or ( i.link_url == '/' and current_path == '/' )
        if not i.login_required or ( i.login_required and user.is_authenticated() ):
            menuitems.append({'url': i.link_url, 'title': i.title, 'current': current,})
    return menuitems

def check_class(parser, token):
    try:
        tag_name, menu_item = token.split_contents()

    except: 
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % token.contents.split()[0]

    return CSSClass(menu_item)

class CSSClass(template.Node):
        
    path_starts = {
            'home': '/', 
            'about': ['/faq', '/board', '/press', '/staff', '/methodology'],
            'subsidy_types': ['/tax-subsidies', '/grants', '/contracts', '/loans' ],
            'sectors': ['/bailout', '/transportation', '/nonprofits', '/energy', '/housing', '/health'],
            'data': ['/tax_expenditures', '/glossary', '/documents', '/data'],
            'contact':['/contact'] 
        }
    def __init__(self, menu_item):
        self.menu_item = menu_item

    def render(self, context):
        current_path = template.resolve_variable('request.path', context)
        if self.menu_item == "home" and current_path != "/":
            return ''
        else:
            for path_start in CSSClass.path_starts[self.menu_item]:
                if current_path.startswith(path_start):
                    return 'active_section'

        return ''

register.tag('menu', build_menu)
register.tag('submenu', build_sub_menu)
register.tag('check_active_class', check_class)
register.inclusion_tag('menu/secondary.html', takes_context=True)(recursive_menu)