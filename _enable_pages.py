"""Enable GitHub Pages on the repo."""
import subprocess, requests, sys, json, time
sys.stdout.reconfigure(encoding='utf-8')

proc = subprocess.Popen(['git', 'credential', 'fill'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, _ = proc.communicate(input='protocol=https\nhost=github.com\n\n', timeout=15)
token = None
for line in stdout.strip().split('\n'):
    if line.startswith('password='):
        token = line.split('=', 1)[1]
        break

h = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github+json'}

# Enable Pages
r = requests.post(
    'https://api.github.com/repos/bariaspromo/dipsa-ot-form/pages',
    headers=h,
    json={'source': {'branch': 'master', 'path': '/'}},
    timeout=30
)
print(f'Enable Pages: {r.status_code}')
if r.status_code == 409:
    print('Pages ya estaba habilitado')
elif r.ok:
    print('Pages habilitado exitosamente')
else:
    print(r.text[:400])

# Check Pages status
time.sleep(3)
r = requests.get('https://api.github.com/repos/bariaspromo/dipsa-ot-form/pages', headers=h, timeout=30)
if r.ok:
    data = r.json()
    url = data.get('html_url', 'pending')
    status = data.get('status', 'unknown')
    print(f'Pages URL: {url}')
    print(f'Status: {status}')
else:
    print(f'Pages check: {r.status_code}')
    print(r.text[:200])
