def encode_dictionary(params):
    """converts the values of a dictionary to unicode string."""
    if isinstance(params, dict):
        new_dict = params.copy()
        charset = params.get('charset', None)
        for key, val in params.items():
            if not isinstance(val, basestring):
                continue
            new_dict[key] = convert_to_unicode(val, charset)

    else:
        raise TypeError('Parameters must be a dictionary')

    return new_dict


def convert_to_unicode(text, charset='utf-8'):
    '''returns unicode object of text.'''
    if isinstance(text, unicode):
        return text

    if isinstance(text, str):
        try:
            return unicode(text, charset, 'replace')

        except (TypeError, LookupError):
            return unicode(text, 'utf-8', 'replace')

    else:
        raise TypeError('Text must be a string or unicode object.')
