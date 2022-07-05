import subprocess

subprocess.call(['git', 'config', '--local', 'user.email', 'dartbird.yu@gmail.com'])
subprocess.call(['git', 'config', '--local', 'user.name', 'dart-bird(auto)'])
subprocess.call(['git', 'remote', 'remove', 'origin'])
subprocess.call(['git', 'remote', 'add', 'origin', 'https://${{secrets.GIT_TOKEN}}@github.com/dart-bird/korea-subway-stations.git'])
subprocess.call(['git', 'pull', 'origin', 'main'])
subprocess.call(['git', 'add', '*.json'])
subprocess.call(['git', 'commit', '-m', '"Auto - Update Korea stations data"'])
subprocess.call(['git', 'push', 'origin', 'main', '-f'])
