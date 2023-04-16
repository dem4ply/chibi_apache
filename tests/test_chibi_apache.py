#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from chibi.file import Chibi_path
from chibi.file.temp import Chibi_temp_path
from chibi_apache import Chibi_apache
from chibi_apache.apache import parse, to_string

expected_default = {
    'AddDefaultCharset': 'UTF-8',
    'Directory': {
        '"/var/www"': {
            'AllowOverride': 'None',
            'Require': 'all granted'
        },
        '"/var/www/cgi-bin"': {
            'AllowOverride': 'None',
            'Options': 'None',
            'Require': 'all granted'
        },
        '"/var/www/html"': {
            'AllowOverride': 'None',
            'Options': 'Indexes FollowSymLinks',
            'Require': 'all granted'
        },
        '/': {
            'AllowOverride': 'none',
            'Require': 'all denied'
        }
    },
    'DocumentRoot': '"/var/www/html"',
    'EnableSendfile': 'on',
    'ErrorLog': '"logs/error_log"',
    'Files': {'".ht*"': {'Require': 'all denied'}},
    'Group': 'apache',
    'IfModule': {
        'alias_module': {
            'ScriptAlias': '/cgi-bin/ "/var/www/cgi-bin/"'
        },
        'dir_module': {
            'DirectoryIndex': 'index.html'
        },
        'log_config_module': {
            'CustomLog': '"logs/access_log" combined',
            'IfModule': {
                'logio_module': {
                    'LogFormat': (
                        r'"%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" '
                        r'\"%{User-Agent}i\" %I %O" combinedio' )
                }
            },
            'LogFormat': [
                ( r'"%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" '
                  r'\"%{User-Agent}i\"" combined' ),
                r'"%h %l %u %t \"%r\" %>s %b" common'
            ]
        },
        'mime_magic_module': {
            'MIMEMagicFile': 'conf/magic'
        },
        'mime_module': {
            'AddOutputFilter': 'INCLUDES .shtml',
            'AddType': [
                'application/x-compress .Z',
                'application/x-gzip .gz .tgz',
                'text/html .shtml'
            ],
            'TypesConfig': '/etc/mime.types'
        }
    },
    'Include': 'conf.modules.d/*.conf',
    'IncludeOptional': 'conf.d/*.conf',
    'Listen': '80',
    'LogLevel': 'warn',
    'ServerAdmin': 'root@localhost',
    'ServerRoot': '"/etc/httpd"',
    'User': 'apache'
}

class Test_chibi_apache( unittest.TestCase ):
    def setUp(self):
        self.file_service = Chibi_path( 'tests/default.conf' )
        self.content = Chibi_path( 'tests/default.conf' ).open().read()
        self.content_clean = Chibi_path(
            'tests/default_clean.conf' ).open().read()

    def tearDown(self):
        pass

    def test_parse_should_work(self):
        data = parse( self.content )
        self.assertEqual( data, expected_default )

    def test_to_string_should_work(self):
        data = parse( self.content )
        result = to_string( data )
        self.maxDiff = None
        self.assertEqual( result, self.content_clean )


class Test_chibi_apache_file( unittest.TestCase ):
    def setUp( self ):
        self.file_service = Chibi_path( 'tests/default.conf' )
        self.expected = expected_default

    def test_should_be_a_dict( self ):
        service = Chibi_apache( self.file_service )
        result = service.read()
        self.assertIsInstance( result, dict )

    def test_should_be_the_expected( self ):
        service = Chibi_apache( self.file_service )
        result = service.read()
        self.assertEqual( result, self.expected )

    def test_write_should_work( self ):
        service = Chibi_apache( self.file_service )
        result = service.read()
        service.write( result )
        result_after_save = service.read()
        self.assertEqual( result, result_after_save )
