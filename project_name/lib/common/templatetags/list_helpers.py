from django.template import Library

register = Library()


@register.filter
def pluck(items, attr):
    def pluck_attr(item):
        if hasattr(item, 'get'):
            return item.get(attr)

        if hasattr(item, attr):
            return item.attr

        raise ValueError('Item `%s` has no attribute `%s`' % (item, attr))

    return [
        pluck_attr(item) for item in items
    ]


@register.filter(name='sum')
def sum_items(items):
    return sum(items)


@register.filter(name='groupby')
def group_by(items, number):
    return [
        items[index:index + number] for index in xrange(0, len(items), number)
    ]


@register.filter(name='split')
def split_list(items, size):
    output = [[] for x in xrange(0, size)]

    for index, item in enumerate(items):
        output[index % size].append(item)

    return output


@register.filter
def lookup(d, key):
    return d[key]