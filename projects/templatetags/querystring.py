from django import template 

register = template.Library() # Creating a Library instance: To use the template.Library() class, 
                              # you need to create an instance of it. This instance will be used to register 
                              # custom template tags and filters.

@register.simple_tag(takes_context=True) # Registers the function as a Django template tag that accepts a context argument.
def query_transform(context, **kwargs):
    
    """Build a querystring from current request.GET.
    Removes existing 'page' param, then adds given params (e.g. page=2).
    Returns the encoded string WITHOUT leading '?'."""
    
    request = context.get('request')
    if not request:
        return ''

    query = request.GET.copy()
    query.pop('page', None)  # remove old page param

    for key, value in kwargs.items():
        query[key] = value

    return query.urlencode()