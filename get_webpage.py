from urllib2 import urlopen, HTTPError


def massage_data(data):
    """return the data that is passed"""
    return data


def get_webform_content(url):
    """Return the contents of a WebForm."""
    try:
        url_content = urlopen(url).read()
        url_content_unicode = url_content.decode('iso-8859-1')
        return massage_data(url_content_unicode)

    except HTTPError:
        print 'HTTP error when retrieving %s' % url
        return False
