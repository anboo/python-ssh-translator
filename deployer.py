import os
import paramiko

server = 'server'
username = 'root'
password = 'password'
localpath = '/var/public/basic'
remotepath = '/var/public/basic'
git_repository_addr = ''

commands = [
    'sudo -S apt-get install nginx',
    'git init',
    'git remote add origin %s' % git_repository_addr,
    'git pull origin master',
    'composer install',
    'chmod 777 -R app/cache app/logs',
    'apt-get remote python',
    'find /var/public/deployer.py -delete'
]

ignore_dirs = [
    '.git',
    '.idea',
    'vendor',
    'node_modules',
    'bower_components'
]

config_local_remote_path = [
    ['/etc/nginx/sites-enabled', '/etc/nginx/sites-enabled'],
    ['/etc/nginx-sites-available', '/etc/nginx/sites-available'],
    ['/var/public/basic', '/var/public/basic']
]

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.connect(server, username=username)
sftp = ssh.open_sftp()

for info in config_local_remote_path:
    localpath = info[0]
    remotepath = info[1]

    for dirpath, dirnames, filenames in os.walk(localpath):
        if dirpath in ignore_dirs:
            continue
        remote_path = os.path.join(remotepath, dirpath)
        sftp.mkdir(remote_path)
        print "%s\n" % remote_path
        # make remote directory ...
        for filename in filenames:
            local_path = os.path.join(dirpath, filename)
            remote_fliepath = os.path.join(remote_path, filename)
            sftp.put(local_path, remote_fliepath)

    for command in commands:
        stdout, stdin, stderr = ssh.exec_command('echo %s | sudo -S %s' % (password, command))
        print stdout

sftp.close()
ssh.close()

