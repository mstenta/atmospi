# Build our default node.
node 'default' {

  # Set some defaults for Exec and File resource types.
  Exec { path => "/usr/sbin/:/sbin:/usr/bin:/bin" }
  File { owner => 'root', group => 'root' }

  # Make sure apt-get update is run before any packages are installed.
  Package { require => Exec['apt-get update'] }
  exec { 'apt-get update':
    command => '/usr/bin/apt-get update',
  }

  # Install vim.
  package { 'vim':
    ensure => latest,
  }

  # Set the timezone.
  file { '/etc/localtime':
    ensure => link,
    target => "/usr/share/zoneinfo/America/New_York",
  }
  file { '/etc/timezone':
    ensure => present,
    content => "America/New_York",
  }

  # Set the default locale.
  file { '/etc/default/locale':
    ensure => present,
    content => 'LANG="en_US.UTF-8"',
  }

  # Install SQLite3
  package { 'sqlite3':
    ensure => latest,
  }

  # Install Apache and mod_wsgi.
  package { ['apache2', 'libapache2-mod-wsgi']:
    ensure => latest,
  }

  # Install Python PIP.
  package { 'python-pip':
    ensure => latest,
  }

  # Use PIP to install Flask.
  exec { 'pip-install-flask':
    command => 'pip install flask',
    require => Package['python-pip'],
    unless => 'pip freeze | grep "Flask"',
  }

  # Symlink the atmospi virtual host into Apache.
  file { 'atmospi-vhost':
    path => '/etc/apache2/sites-enabled/000-atmospi',
    ensure => 'link',
    target => '/home/pi/atmospi/atmospi.vhost',
    require => Package['libapache2-mod-wsgi'],
  }

  # Restart Apache.
  exec { 'apache2ctl restart':
    require => File['atmospi-vhost'],
  }

  # Set up cron jobs.
  cron { 'measure-ds18b20':
    command => '/home/pi/atmospi/Atmospi/measure-ds18b20.py >/dev/null 2>&1',
    user => root,
    minute => '*/5',
  }
}

