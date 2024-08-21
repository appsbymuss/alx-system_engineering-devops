# Sky is the limit, let's bring that limit higher

exec {'15 to 4096':
  command => 'sudo sed -i "s/15/4096/g" /etc/default/nginx',
  path    => ['/usr/bin', '/bin'],
}

exec {'start-nginx':
  command => 'sudo service nginx restart',
  path    => ['/usr/bin', '/bin'],
}
