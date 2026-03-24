"""Create GitHub repo and push content for GitHub Pages."""
import subprocess, json, sys, requests
sys.stdout.reconfigure(encoding='utf-8')

# Get stored GitHub token from credential manager
proc = subprocess.Popen(
    ['git', 'credential', 'fill'],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
)
stdout, stderr = proc.communicate(input='protocol=https\nhost=github.com\n\n', timeout=15)
token = None
for line in stdout.strip().split('\n'):
    if line.startswith('password='):
        token = line.split('=', 1)[1]
        break

if not token:
    print('ERROR: No se encontro token de GitHub en credential manager')
    sys.exit(1)

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Check who we are
r = requests.get('https://api.github.com/user', headers=headers, timeout=15)
if not r.ok:
    print(f'Auth error {r.status_code}: {r.text[:200]}')
    sys.exit(1)
username = r.json()['login']
print(f'Autenticado como: {username}')

# Create private repo
repo_name = 'dipsa-ot-form'
r = requests.post(
    'https://api.github.com/user/repos',
    headers=headers,
    json={
        'name': repo_name,
        'description': 'Formulario Ordenes de Trabajo - DIPSA Operaciones',
        'private': True,
        'has_issues': False,
        'has_projects': False,
        'has_wiki': False
    },
    timeout=30
)

if r.status_code == 201:
    data = r.json()
    print(f'Repo creado: {data["html_url"]}')
    clone_url = data['clone_url']
elif r.status_code == 422 and 'already exists' in r.text:
    print(f'Repo ya existe: https://github.com/{username}/{repo_name}')
    clone_url = f'https://github.com/{username}/{repo_name}.git'
else:
    print(f'Error {r.status_code}: {r.text[:400]}')
    sys.exit(1)

# Enable GitHub Pages on main branch (root)
print('Habilitando GitHub Pages...')
r = requests.post(
    f'https://api.github.com/repos/{username}/{repo_name}/pages',
    headers={**headers, 'Accept': 'application/vnd.github+json'},
    json={
        'source': {
            'branch': 'master',
            'path': '/'
        }
    },
    timeout=30
)
if r.status_code in (201, 409):
    print('GitHub Pages habilitado')
else:
    print(f'Pages config: {r.status_code} (se puede habilitar manualmente)')

# Print the URL
pages_url = f'https://{username}.github.io/{repo_name}/'
print(f'\nURL del formulario: {pages_url}')
print(f'Clone URL: {clone_url}')
