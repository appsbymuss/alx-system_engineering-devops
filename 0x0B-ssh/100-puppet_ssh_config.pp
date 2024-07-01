# SSH client configuration for a specific host

file_line { 'set SSH client options':
	path    => '/etc/ssh/ssh_config',
	line    => '	PasswordAuthentication no',
	ensure  => present,
}

file_line { 'add SSH IdentityFile':
	path    => '/etc/ssh/ssh_config',
	line    => '	IdentityFile ~/.ssh/school',
	ensure  => present,
}
