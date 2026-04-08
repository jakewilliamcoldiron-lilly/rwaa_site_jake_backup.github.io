import csv, io
from collections import defaultdict

raw = open('/mnt/user-data/uploads/dat_rwaa_sa_team.xlsx').read()
reader = csv.DictReader(io.StringIO(raw))
rows = [r for r in reader if r['ta'] and r['ta'] != 'NA']

def pretty(s):
    s = s.replace('_', ' ')
    fixes = {
        'xinran flora luo': 'Xinran (Flora) Luo',
        'xiaohong ivy li':  'Xiaohong (Ivy) Li',
        'alexandra zan meeks': 'Alexandra (Zan) Meeks',
        'jake william coldiron': 'Jake William Coldiron',
    }
    return fixes.get(s, s.title())

score_cols = ['optum','health_verity','ibd_plexus','komodo','truveta','flatiron',
              'iqvia','tri_net_x','nhis','welldoc','meps','nhanes','cprd',
              'ihd','aetion','sas','r']

score_labels = {
    'optum':'Optum','health_verity':'HealthVerity','ibd_plexus':'IBD Plexus',
    'komodo':'Komodo','truveta':'Truveta','flatiron':'Flatiron','iqvia':'IQVIA',
    'tri_net_x':'TriNetX','nhis':'NHIS','welldoc':'WellDoc','meps':'MEPS',
    'nhanes':'NHANES','cprd':'CPRD','ihd':'IHD','aetion':'Aetion','sas':'SAS','r':'R',
}

db_keys   = ['optum','health_verity','ibd_plexus','komodo','truveta','flatiron',
             'iqvia','tri_net_x','nhis','welldoc','meps','nhanes','cprd']
tool_keys = ['ihd','aetion','sas','r']

groups = defaultdict(lambda: {'head': None, 'leads': [], 'members': []})
seen = set()

for r in rows:
    ta, fg, role, name, emp = r['ta'], r['fg'], r['role'], r['name'], r['emp']
    pt  = emp == 'pt'
    key = (ta, fg)
    dedup = (name, ta, fg, role)
    if dedup in seen:
        continue
    seen.add(dedup)
    scores = {c: int(r[c]) if r.get(c) and r[c] not in ('NA','') else 1 for c in score_cols}
    entry = {'name': pretty(name), 'emp': emp, 'pt': pt, 'scores': scores}
    if role == 'head':
        groups[key]['head'] = entry
    elif role == 'lead':
        groups[key]['leads'].append(entry)
    else:
        groups[key]['members'].append(entry)

ta_colors = {
    'immuno':       {'header': '#0F6E56', 'light': '#d0f0e6'},
    'neuro':        {'header': '#534AB7', 'light': '#e8e6f9'},
    'cmh':          {'header': '#185FA5', 'light': '#daeeff'},
    'onco':         {'header': '#993C1D', 'light': '#fde8df'},
    'capabilities': {'header': '#854F0B', 'light': '#fdf0d5'},
}
ta_labels = {'immuno':'Immunology','neuro':'Neurology','cmh':'CMH','onco':'Oncology','capabilities':'Capabilities'}
fg_labels = {'heor':'HEOR','hta':'HTA','gps':'GPS','capabilities':'All'}
gps_tags  = {('cmh','heor'),('neuro','hta'),('onco','heor'),('onco','hta'),('capabilities','capabilities')}

def scores_attr(scores):
    return ' '.join(f'data-{k}="{v}"' for k, v in scores.items())

def member_row_emp(m, bold=False):
    weight = 'font-weight:600;' if bold else ''
    style  = f'font-size:11.5px;padding:2px 0;line-height:1.5;display:flex;align-items:center;gap:5px;flex-wrap:wrap;color:#1a1a1a;{weight}'
    badges = ''
    if m['emp'] == 'ct':
        badges += '<span class="emp-badge" style="font-size:9px;padding:1px 5px;border-radius:999px;background:#e5e5e5;color:#555;">Contractor</span>'
    if m['pt']:
        badges += '<span class="emp-badge" style="font-size:9px;padding:1px 5px;border-radius:999px;background:#e5e5e5;color:#555;">Part-Time</span>'
    sa = scores_attr(m['scores'])
    return f'<div data-emp="{m["emp"]}" {sa} style="{style}">{m["name"]}{badges}<span class="exp-badge"></span></div>'

def make_card(ta, fg, group_data, gps_head=None):
    colors      = ta_colors[ta]
    header_text = f'{ta_labels[ta]} – {fg_labels[fg]}'
    gps_html    = ' &amp; <span style="color:#ff6b6b;">GPS</span>' if gps_head else ''
    head        = group_data['head']
    leads       = group_data['leads']
    members     = group_data['members']
    head_html   = ''
    if head:
        gps_style = 'color:#CC0000;' if gps_head else 'color:#1a1a1a;'
        sa = scores_attr(head['scores'])
        emp_badge = ''
        if head['emp'] == 'ct':
            emp_badge = '<span class="emp-badge" style="font-size:9px;padding:1px 5px;border-radius:999px;background:#e5e5e5;color:#555;">Contractor</span>'
        if head['pt']:
            emp_badge = '<span class="emp-badge" style="font-size:9px;padding:1px 5px;border-radius:999px;background:#e5e5e5;color:#555;">Part-Time</span>'
        head_html = f'<div data-emp="{head["emp"]}" {sa} style="padding:4px 10px;font-size:12px;font-weight:600;text-align:center;border-bottom:0.5px solid rgba(0,0,0,0.1);{gps_style}">{head["name"]}{emp_badge}<span class="exp-badge"></span></div>'
    leads_html = ''
    if leads:
        leads_rows = ''.join(member_row_emp(m, bold=True) for m in leads)
        leads_html = f'<div style="padding:4px 10px 6px;border-bottom:0.5px solid rgba(0,0,0,0.1);">{leads_rows}</div>'
    members_html    = ''.join(member_row_emp(m, bold=False) for m in members)
    members_section = f'<div style="padding:4px 10px 8px;">{members_html}</div>' if members else ''
    return f'<div style="border-radius:8px;overflow:hidden;border:0.5px solid rgba(0,0,0,0.12);background:{colors["light"]};"><div style="background:{colors["header"]};color:#fff;padding:7px 10px 4px;font-size:12px;font-weight:500;line-height:1.3;">{header_text}{gps_html}</div>{head_html}{leads_html}{members_section}</div>'

row1_keys = [('immuno','heor'),('neuro','heor'),('cmh','heor'),('onco','heor'),('capabilities','capabilities')]
row2_keys = [('immuno','hta'),('neuro','hta'),('cmh','hta'),('onco','hta')]

def render_row(keys, extra_cols=0):
    cards   = ''.join(make_card(k[0], k[1], groups[k], k in gps_tags) for k in keys if k in groups)
    spacers = ''.join('<div></div>' for _ in range(extra_cols))
    return f'<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-bottom:10px;">{cards}{spacers}</div>'

def db_buttons():
    btns = '<button class="filter-btn active" onclick="setExpKey(\'\',this)">All</button>'
    for k in db_keys:
        btns += f'<button class="filter-btn" onclick="setExpKey(\'{k}\',this)">{score_labels[k]}</button>'
    return btns

def tool_buttons():
    btns = '<button class="filter-btn active" onclick="setExpKey(\'\',this)">All</button>'
    for k in tool_keys:
        btns += f'<button class="filter-btn" onclick="setExpKey(\'{k}\',this)">{score_labels[k]}</button>'
    return btns

html_final = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>RWAA SA Team</title>
<style>
  body {{font-family:system-ui,sans-serif;background:#fff;color:#1a1a1a;margin:0;padding:1.5rem;}}
  .org-title {{background:#2C3E50;color:white;text-align:center;font-size:18px;font-weight:500;padding:10px 16px;border-radius:8px;margin-bottom:1rem;}}
  .stats-bar {{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:1.2rem;}}
  .stat-pill {{background:#f5f5f5;border:0.5px solid #ddd;border-radius:999px;padding:4px 14px;font-size:13px;color:#555;}}
  .stat-pill strong {{color:#1a1a1a;}}
  .filter-section {{margin-bottom:1.2rem;}}
  .filter-row {{display:flex;gap:6px;flex-wrap:wrap;align-items:center;margin-bottom:6px;}}
  .filter-label {{font-size:12px;color:#555;font-weight:500;min-width:100px;flex-shrink:0;}}
  .filter-btn {{font-size:11px;padding:3px 10px;border:0.5px solid #bbb;border-radius:999px;background:transparent;color:#1a1a1a;cursor:pointer;}}
  .filter-btn:hover {{background:#f0f0f0;}}
  .filter-btn.active     {{background:#2C3E50;color:#fff;border-color:transparent;}}
  .filter-btn.active-user{{background:#3b82f6;color:#fff;border-color:transparent;}}
  .filter-btn.active-pro {{background:#7c3aed;color:#fff;border-color:transparent;}}
  .proficiency-row {{opacity:0.35;pointer-events:none;transition:opacity 0.2s;}}
  .proficiency-row.enabled {{opacity:1;pointer-events:all;}}
  [data-emp].hidden {{display:none!important;}}
  .badge-user {{font-size:9px;padding:1px 5px;border-radius:999px;background:#dbeafe;color:#1d4ed8;}}
  .badge-pro  {{font-size:9px;padding:1px 5px;border-radius:999px;background:#ede9fe;color:#6d28d9;}}
  .legend {{display:flex;gap:14px;flex-wrap:wrap;margin-top:1rem;font-size:12px;color:#666;}}
  .legend-item {{display:flex;align-items:center;gap:5px;}}
  .legend-dot {{width:10px;height:10px;border-radius:50%;flex-shrink:0;}}
</style>
</head>
<body>
<div class="org-title">RWAA SA Team</div>
<div class="stats-bar">
  <div class="stat-pill"><strong>56</strong> analysts total</div>
  <div class="stat-pill"><strong>19</strong> FTEs</div>
  <div class="stat-pill"><strong>37</strong> contractors</div>
  <div class="stat-pill"><strong>51</strong> certified SAS programmers</div>
  <div class="stat-pill"><strong>9</strong> certified IHD users</div>
  <div class="stat-pill"><strong>8</strong> Aetion users</div>
  <div class="stat-pill"><strong>52</strong> active R users</div>
</div>
<div class="filter-section">
  <div class="filter-row">
    <span class="filter-label">Employment:</span>
    <button class="filter-btn active" onclick="setEmp('all',this)">All</button>
    <button class="filter-btn" onclick="setEmp('ft',this)">Full-Time</button>
    <button class="filter-btn" onclick="setEmp('pt',this)">Part-Time</button>
    <button class="filter-btn" onclick="setEmp('ct',this)">Contractors</button>
  </div>
  <div class="filter-row" id="db-row">
    <span class="filter-label">Databases:</span>
    {db_buttons()}
  </div>
  <div class="filter-row" id="tool-row">
    <span class="filter-label">Tools:</span>
    {tool_buttons()}
  </div>
  <div class="filter-row proficiency-row" id="prof-row">
    <span class="filter-label">Proficiency:</span>
    <button class="filter-btn active" onclick="setExpLevel('',this)">All</button>
    <button class="filter-btn" onclick="setExpLevel('user',this)">User</button>
    <button class="filter-btn" onclick="setExpLevel('pro',this)">Professional</button>
  </div>
</div>
{render_row(row1_keys)}
{render_row(row2_keys, extra_cols=1)}
<div class="legend">
  <div class="legend-item"><div class="legend-dot" style="background:#0F6E56;"></div> Immunology</div>
  <div class="legend-item"><div class="legend-dot" style="background:#185FA5;"></div> CMH</div>
  <div class="legend-item"><div class="legend-dot" style="background:#534AB7;"></div> Neurology</div>
  <div class="legend-item"><div class="legend-dot" style="background:#993C1D;"></div> Oncology</div>
  <div class="legend-item"><div class="legend-dot" style="background:#854F0B;"></div> Capabilities</div>
  <div class="legend-item"><div class="legend-dot" style="background:#3b82f6;"></div> User (level 2)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#7c3aed;"></div> Professional (level 3)</div>
  <div class="legend-item"><div class="legend-dot" style="background:#CC0000;"></div> GPS-aligned head</div>
</div>
<script>
let empFilter = 'all';
let expKey    = '';
let expLevel  = '';

function setEmp(type, btn) {{
  document.querySelectorAll('#db-row .filter-btn, [onclick^="setEmp"]').forEach(b => {{
    if (b.getAttribute('onclick') && b.getAttribute('onclick').startsWith('setEmp')) b.classList.remove('active');
  }});
  btn.classList.add('active');
  empFilter = type;
  apply();
}}

function setExpKey(key, btn) {{
  // Clear active from both db and tool rows
  document.querySelectorAll('#db-row .filter-btn, #tool-row .filter-btn').forEach(b => b.classList.remove('active','active-user','active-pro'));
  btn.classList.add('active');
  expKey = key;
  // Enable/disable proficiency row
  const profRow = document.getElementById('prof-row');
  if (key) {{
    profRow.classList.add('enabled');
  }} else {{
    profRow.classList.remove('enabled');
    expLevel = '';
    document.querySelectorAll('#prof-row .filter-btn').forEach((b,i) => b.classList.toggle('active', i===0));
  }}
  apply();
}}

function setExpLevel(level, btn) {{
  document.querySelectorAll('#prof-row .filter-btn').forEach(b => b.classList.remove('active','active-user','active-pro'));
  if (!level) {{ btn.classList.add('active'); }}
  else {{ btn.classList.add(level === 'pro' ? 'active-pro' : 'active-user'); }}
  expLevel = level;
  apply();
}}

function apply() {{
  document.querySelectorAll('[data-emp]').forEach(el => {{
    let show = true;
    if (empFilter !== 'all' && el.dataset.emp !== empFilter) show = false;
    if (expKey) {{
      const val = parseInt(el.dataset[expKey] || '1');
      if (expLevel === 'user' && val < 2) show = false;
      if (expLevel === 'pro'  && val < 3) show = false;
    }}
    el.classList.toggle('hidden', !show);
    const badge = el.querySelector('.exp-badge');
    if (badge) {{
      badge.className = 'exp-badge';
      badge.textContent = '';
      if (expKey && !el.classList.contains('hidden')) {{
        const val = parseInt(el.dataset[expKey] || '1');
        if (val >= 3)      {{ badge.className = 'exp-badge badge-pro';  badge.textContent = 'Professional'; }}
        else if (val === 2) {{ badge.className = 'exp-badge badge-user'; badge.textContent = 'User'; }}
      }}
    }}
  }});
}}
</script>
</body>
</html>'''

with open('/mnt/user-data/outputs/rwaa-org-chart.html', 'w') as f:
    f.write(html_final)
print('Done')
