"""Make repo public and enable GitHub Pages."""
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
repo = 'bariaspromo/dipsa-ot-form'

# Step 1: Make repo public
print('Cambiando repo a publico...')
r = requests.patch(
    f'https://api.github.com/repos/{repo}',
    headers=h,
    json={'private': False},
    timeout=30
)
if r.ok:
    print('Repo ahora es publico')
else:
    print(f'Error: {r.status_code} - {r.text[:300]}')
    sys.exit(1)

# Step 2: Enable Pages
time.sleep(2)
print('Habilitando GitHub Pages...')
r = requests.post(
    f'https://api.github.com/repos/{repo}/pages',
    headers=h,
    json={'source': {'branch': 'master', 'path': '/'}},
    timeout=30
)
if r.status_code in (201, 409):
    print('GitHub Pages habilitado')
else:
    print(f'Pages: {r.status_code} - {r.text[:300]}')

# Step 3: Check status
time.sleep(5)
r = requests.get(f'https://api.github.com/repos/{repo}/pages', headers=h, timeout=30)
if r.ok:
    data = r.json()
    url = data.get('html_url', 'pending')
    status = data.get('status', 'unknown')
    print(f'URL: {url}')
    print(f'Status: {status}')
else:
    print(f'Check: {r.status_code} - {r.text[:200]}')
