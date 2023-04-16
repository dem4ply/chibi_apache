============
chibi_apache
============


.. image:: https://img.shields.io/pypi/v/chibi_apache.svg
        :target: https://pypi.python.org/pypi/chibi_apache

.. image:: https://img.shields.io/travis/dem4ply/chibi_apache.svg
        :target: https://travis-ci.org/dem4ply/chibi_apache

.. image:: https://readthedocs.org/projects/chibi-apache/badge/?version=latest
        :target: https://chibi-apache.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




libreria para leer y escribir los archivos de configuracion de apache


* Free software: WTFPL
* Documentation: https://chibi-apache.readthedocs.io.


=======
Install
=======


.. code-block:: bash

	pip install chibi-apache


=====
Usage
=====


.. code-block:: bash

	cat > /etc/httpd/conf/httpd.conf << 'endmsg'
	ServerRoot "/etc/httpd"
	Listen 80
	Include conf.modules.d/*.conf
	User apache
	Group apache
	ServerAdmin root@localhost

	<Directory />
		AllowOverride none
		Require all denied
	</Directory>

	<Directory "/var/www">
		AllowOverride None
		Require all granted
	</Directory>

	<Directory "/var/www/html">
		Options Indexes FollowSymLinks
		AllowOverride None
		Require all granted
	</Directory>

	<Directory "/var/www/cgi-bin">
		AllowOverride None
		Options None
		Require all granted
	</Directory>
	DocumentRoot "/var/www/html"

	<IfModule dir_module>
		DirectoryIndex index.html
	</IfModule>

	<IfModule log_config_module>
		LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
		LogFormat "%h %l %u %t \"%r\" %>s %b" common

		<IfModule logio_module>
			LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %I %O" combinedio
		</IfModule>
		CustomLog "logs/access_log" combined
	</IfModule>

	<IfModule alias_module>
		ScriptAlias /cgi-bin/ "/var/www/cgi-bin/"
	</IfModule>

	<IfModule mime_module>
		TypesConfig /etc/mime.types
		AddType application/x-compress .Z
		AddType application/x-gzip .gz .tgz
		AddType text/html .shtml
		AddOutputFilter INCLUDES .shtml
	</IfModule>

	<IfModule mime_magic_module>
		MIMEMagicFile conf/magic
	</IfModule>

	<Files ".ht*">
		Require all denied
	</Files>
	ErrorLog "logs/error_log"
	LogLevel warn
	AddDefaultCharset UTF-8
	EnableSendfile on
	IncludeOptional conf.d/*.conf
	endmsg


.. code-block:: python

	from chibi_apache import Chibi_apache

	tmp = Chibi_nginx( '/etc/httpd/conf/httpd.conf' )
	result = tmp.read()
	expected = {
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

	assert result == expected

	result.pop( 'User' )
	result.User = 'root'
	tmp.write( result )
	new_result = tmp.read()
	assert new_result.User == 'root'

	result.Directory.pop( '"/var/www/cgi-bin"' )
	tmp.write( result )
	new_result = tmp.read()
	assert '"/var/www/cgi-bin"' not in new_result[ 'Directory' ]


Features
--------

* read and write config files of apache httpd
