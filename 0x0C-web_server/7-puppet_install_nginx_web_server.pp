# install nginx
package { 'nginx':
  ensure => installed,
}

# website index file
file { '/var/www/html/index.html':
  content => 'Hello World!',
}

# redirect_me config
file_line { 'redirect_me':
  ensure => present,
  path   => '/etc/nginx/sites-available/default',
  after  => 'server_name _;',
  line   => '
        location /redirect_me {
            return 301 https://www.youtube.com/watch?v=QH2-TGUlwu4;
            # Am omar but you can call me dehao
        }',
}

# stop nginx
exec { 'stop service':
  command => 'sudo service nginx stop',
  path    => ['/bin', '/usr/bin', '/usr/sbin'],
}

# run nginx
exec { 'start service':
  command => 'sudo service nginx start',
  path    => ['/bin', '/usr/bin', '/usr/sbin'],
}
