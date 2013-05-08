from unittest2 import TestCase

from methods import encode_dictionary, convert_to_unicode


class WhenEncodingDictionaries(TestCase):

    def test_should_require_arguments(self):
        self.assertRaises(TypeError, encode_dictionary)

    def test_should_argument_be_a_dictionary(self):
        self.assertRaises(TypeError, encode_dictionary, '')

    def test_should_return_new_dictionary(self):
        params = {'key': 'value'}
        result = encode_dictionary(params)

        self.assertTrue(isinstance(result, dict))
        self.assertTrue(result is not params)

    def test_should_return_new_dictionary_with_unicode_values(self):
        params = {'key': 'value'}
        result = encode_dictionary(params)
        self.assertDictEqual(result, {'key': u'value'})

    def test_should_find_charset_in_params(self):
        default_data = {
            'txn_type': 'express_checkout',
            'payment_status': 'Completed',
            'first_name': 'Bob',
            'last_name': 'Smith',
            'payer_email': 'bob@example.com',
            'item_name1': 'not-a-rule',
            'item_number': 123,
            'charset': 'ascii'
        }
        result = encode_dictionary(default_data)
        assert result['charset'] == u'ascii'

    def test_return_dictionary_values_converted_to_unicode(self):
        default_data = {
            'txn_type': 'express_checkout',
            'payment_status': 'Completed',
            'first_name': 'Bob',
            'last_name': 'Smith',
            'payer_email': 'bob@example.com',
            'item_name1': 'not-a-rule',
            'item_number': 123,
            'charset': 'ascii'
        }
        result = encode_dictionary(default_data)

        for key, val in result.items():
            if not isinstance(val, basestring):
                continue
            self.assertIsInstance(val, unicode)


class WhenEncodingStrings(TestCase):

    def test_raise_err_if_original_parm_is_None(self):
        self.assertRaises(TypeError, convert_to_unicode, None)

    def test_raise_err_if_original_param_is_not_string(self):
        self.assertRaises(TypeError, convert_to_unicode, 123)
        self.assertRaises(TypeError, convert_to_unicode, dict())
        self.assertRaises(TypeError, convert_to_unicode, list())

    def test_return_unicode_if_original_param_is_unicode(self):
        mystring = u'This is a unicode string'
        result = convert_to_unicode(mystring, 'utf8')
        self.assertIs(result, mystring)

    def test_convert_ascii_to_unicode(self):
        result = convert_to_unicode('This is an ascii string', 'ascii')
        self.assertEqual(result, u'This is an ascii string')

    def test_convert_capital_thorn_in_latin1_to_unicode(self):
        # DE is capital Thorn in latin1
        result = convert_to_unicode('\xde', 'latin1')
        self.assertEqual(result, u'\u00de')

    def test_convert_capital_thorn_in_cp850_to_unicode(self):
        # E8 is capital Thorn in cp850
        result = convert_to_unicode('\xe8', 'cp850')
        self.assertEqual(result, u'\u00de')

    def test_convert_utf8_chars_to_unicode(self):
        # C3 9E: capital Thorn in UTF-8
        result = convert_to_unicode('\xc3\x9e', 'utf-8')
        self.assertEqual(result, u'\u00de')

    def test_default_to_utf8_if_charset_omitted(self):
        # C3 9E: capital Thorn in UTF-8
        result = convert_to_unicode('\xc3\x9e')
        self.assertEqual(result, u'\u00de')

    def test_default_to_utf8_if_charset_is_none(self):
        # C3 9E: capital Thorn in UTF-8
        result = convert_to_unicode('\xc3\x9e', None)
        self.assertEqual(result, u'\u00de')

    def test_default_to_utf8_if_charset_is_empty_string(self):
        # C3 9E: capital Thorn in UTF-8
        result = convert_to_unicode('\xc3\x9e', '')
        self.assertEqual(result, u'\u00de')

    def test_return_utf8_if_unknown_charset(self):
        # C3 9E: capital Thorn in UTF-8
        result = convert_to_unicode('\xc3\x9e', 'DoesNotExist')
        self.assertEqual(result, u'\u00de')

    def test_replace_chars_not_in_charset_with_replacement_char(self):
        # E0 is not valid in the ascii character set
        result = convert_to_unicode('before \xe0 after', 'ascii')
        assert result == u'before \ufffd after'

    def test_replace_chars_when_assuming_utf8_with_replacement_char(self):
        # C0 00  is not valid in UTF-8
        #result = convert_to_unicode('before \xe0 after')
        result = convert_to_unicode('before \xc0\x00 after')
        print result
        assert result == u'before \ufffd after'
