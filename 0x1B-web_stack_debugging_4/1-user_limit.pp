# User No Limit

exec { 'remove limits':
  command => 'sed -i s/holberton/#/g /etc/security/limits.conf',
  path    => ['/usr/bin', '/bin']
}
