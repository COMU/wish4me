#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db.models.fields.files import ImageFieldFile
from django import template
register = template.Library()


@register.inclusion_tag('_list.html')
def create_list(list_name, query, attrs, *args, **kwargs):
  """Creates a wish4me list (with respect to bootstrap) from given elements.

  {% create_list  list_name  query  attrs  actions  page_index=page_index
     page_count=page_count ajax_paginate_url=ajax_paginate_url %}

  Args:
    list_name: Name of the list that will be shown on top of the list.
    query: A database query or anything that is iterable and contains elements.
    attrs: Attributes and options of each element to show in the columns of
           the list.
           May be a list object or a string that will be evaluated with eval().
           Eg."[ {'profil_photo': {'width': 2}}, {'content': {'width': 3}}, ..]"

  Optional Args:
    actions: List contains strings as name of the actions possible on each element.
             Final URL of the action button will be:
             action_name + element.get_absolute_path()
    page_index: Integer that represents current page.
    page_count: Total pages count.
    ajax_paginate_url: String that represents URL of the AJAX pagination view.
  """

  actions = kwargs.get('actions', None)
  try:
    actions = eval(unicode(actions))
  except:
    pass

  try:
    attrs = eval(unicode(attrs))
  except:
    pass

  page_index = kwargs.get('page_index', None)
  page_count = kwargs.get('page_count', None)
  ajax_paginate_url = kwargs.get('ajax_paginate_url', None)
  if page_index is None:
    paginate = False
  else:
    paginate = True

  lst = []
  for element in query:
    fields = []
    for attr in attrs:
      attr_name, properties = attr.items()[0]
      field = getattr(element, attr_name)
      if field.__class__ == ImageFieldFile:
        field = {'is_thumbnail': True,
                  'path': field.url}
      else:
        field = {'content': field}
      field['width'] = properties['width']
      fields.append(field)
    lst.append(fields)

  return {'list_name': list_name, 'lst': lst, 'paginate': paginate,
          'page_index': page_index, 'page_count': page_count,
          'ajax_paginate_url': ajax_paginate_url}
