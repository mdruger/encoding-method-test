from mock import Mock, patch
from StringIO import StringIO
import unittest2
from urllib2 import HTTPError

from get_webpage import get_webform_content


class WhenReadingWebFormContent(unittest2.TestCase):

    webform_url = "http://www.google.com"

    def test_require_url(self):
        self.assertRaises(TypeError, get_webform_content)

    @patch("get_webpage.urlopen")
    def test_open_correct_webform(self, urlopen):
        urlopen.return_value = StringIO("")
        get_webform_content(self.webform_url)
        urlopen.assert_called_once_with(self.webform_url)

    @patch('get_webpage.massage_data')
    @patch("get_webpage.urlopen")
    def test_read_webform_content(self, urlopen, massage_data):
        get_webform_content(self.webform_url)
        urlopen(self.webform_url).read.assert_called_once_with()

    @patch('get_webpage.massage_data')
    @patch("get_webpage.urlopen")
    def test_return_converted_webform_content(self, urlopen, massage_data):
        massage_data.return_value = 'awesome'
        self.assertEqual(get_webform_content(self.webform_url), 'awesome')

    @patch("get_webpage.urlopen")
    def test_return_false_on_http_errors(self, urlopen):
        urlopen.side_effect = HTTPError('', '', '', '', StringIO(''))
        self.assertFalse(get_webform_content(self.webform_url))

    @patch('get_webpage.massage_data')
    @patch("get_webpage.urlopen")
    def test_decode_url_content_to_unicode(self, urlopen, massage_data):
        mock_url_content = Mock()
        urlopen(self.webform_url).read.return_value = mock_url_content
        get_webform_content(self.webform_url)
        mock_url_content.decode.assert_called_once_with('iso-8859-1')

    @patch('get_webpage.massage_data')
    @patch("get_webpage.urlopen")
    def test_call_massage_data_with_unicode_param(self, urlopen, massage_data):
        mock_url_content = Mock()
        urlopen(self.webform_url).read.return_value = mock_url_content
        get_webform_content(self.webform_url)
        massage_data.assert_called_with(mock_url_content.decode('iso-8859-1'))

    @patch('facebook_canvas.lib.webform_get.support_ssl_webforms')
    @patch('facebook_canvas.lib.webform_get.urlopen')
    def should_rtn_str_with_capital_thorn_in_latin1_to_unicode(self, urlopen,
                                                               ssl_webforms):
        mock_url_content = Mock()
        # DE is capital Thorn in latin1
        mock_url_content.return_value = 'awesome\xde'
        urlopen(self.webform_url).read.return_value = mock_url_content

        # 00de is capital Thorn in latin1 converted to unicode
        ssl_webforms.return_value = u'awesome\u00de'
        self.assertEqual(get_webform_content(98765),
                         mock_url_content.return_value.decode('iso-8859-1'))

    @patch('facebook_canvas.lib.webform_get.urlopen')
    def should_return_webform_content_as_valid_unicode(self, urlopen):
        urlopen.return_value = StringIO('webform_content')
        self.assertIsInstance(get_webform_content(12345), unicode)


if __name__ == '__main__':
    unittest2.main()
