"""Generate the static GitHub Pages portfolio and editable Markdown."""
from pathlib import Path
import json
import html

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
PROFILE = DATA['profile']
OUT = ROOT / 'docs'
OUT.mkdir(exist_ok=True)
esc = html.escape

def lis(items):
    return '<ul>' + ''.join('<li>' + esc(x) + '</li>' for x in items) + '</ul>'

def link(label, url, cls=''):
    return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)} <span aria-hidden="true">↗</span></a>'

def section_title(number, title):
    return f'<h2 class="profile-section-title"><span>{number}</span>{esc(title)}</h2>'

education_rows = ''.join(
    '<tr>' + ''.join(f'<td>{esc(e[key])}</td>' for key in ['school', 'major', 'period', 'status']) + '</tr>'
    for e in PROFILE['education']
)
credential_rows = ''.join(
    f'<tr><td class="credential-type">{esc(c["type"])}</td><td>{esc(c["name"])}</td><td>{esc(c["date"])}</td></tr>'
    for c in PROFILE['credentials']
)
activity_rows = ''.join(
    f'<article class="activity-row"><header class="profile-row-heading"><h3>{esc(a["name"])}</h3><p class="period">{esc(a["period"])}</p></header>{lis(a["items"])}</article>'
    for a in PROFILE['activities']
)
experience = PROFILE['experience']
profile_page = f'''<section class="profile sheet" id="overview" aria-labelledby="profile-name">
  <header class="profile-header"><div class="profile-heading"><h1 id="profile-name">{esc(DATA['name'])}</h1><div class="application-target"><strong>{esc(PROFILE['organization'])}</strong><p>{esc(PROFILE['department'])}</p></div><p class="document-title">{esc(PROFILE['title'])}</p></div><p class="profile-summary">{' <span aria-hidden="true">/</span> '.join(esc(x) for x in PROFILE['summary'])}</p></header>
  <section class="profile-block education">{section_title('01', '학력')}<div class="table-scroll"><table class="profile-table education-table"><caption class="sr-only">학력</caption><colgroup><col class="school-col"><col class="major-col"><col class="period-col"><col class="status-col"></colgroup><thead><tr><th scope="col">학교</th><th scope="col">전공</th><th scope="col">기간</th><th scope="col">비고</th></tr></thead><tbody>{education_rows}</tbody></table></div></section>
  <section class="profile-block activities">{section_title('02', '교내 활동')}{activity_rows}</section>
  <section class="profile-block credentials">{section_title('03', '자격증 및 수료')}<div class="table-scroll"><table class="profile-table credentials-table"><caption class="sr-only">자격증 및 수료 내역</caption><colgroup><col class="type-col"><col><col class="date-col"></colgroup><thead><tr><th scope="col">구분</th><th scope="col">내용</th><th scope="col">취득일</th></tr></thead><tbody>{credential_rows}</tbody></table></div></section>
  <section class="profile-block experience">{section_title('04', '실무 경험')}<div class="experience-row"><header class="profile-row-heading"><h3>{esc(experience['name'])}</h3><p class="period">{esc(experience['period'])}</p></header><p class="experience-details"><span>{esc(experience['items'][0])} / {esc(experience['items'][1])}</span><strong>{esc(experience['items'][2])}</strong></p></div></section>
  <section class="profile-block core-skills">{section_title('05', '핵심 역량')}<ul class="skill-list">{''.join(f'<li>{esc(x)}</li>' for x in PROFILE['competencies'])}</ul></section>
  <p class="print-folio">김재원 · 이지스자산운용 헤지펀드운용파트 지원 포트폴리오 <span>01 / 05</span></p>
</section>'''

nav = '<a class="nav-link active" href="#overview"><span>00</span>프로필 및 핵심 역량</a>' + ''.join(f'<a class="nav-link" href="#{p["id"]}"><span>{p["number"]}</span>{esc(p["title"].replace(" AI 자동화", "").replace(" 운용 시스템", " 운용자료"))}</a>' for p in DATA['projects'])
projects = []
for p in DATA['projects']:
    table = ''
    if p['id'] == 'vfs':
        table = '''<figure class="result-table"><table><caption>VFS−Value 월평균 차이</caption><thead><tr><th scope="col">가중 방식</th><th scope="col">상대성과</th></tr></thead><tbody><tr><th scope="row">시가총액가중</th><td>+0.43%p</td></tr><tr><th scope="row">동일가중</th><td>−0.4158%p</td></tr></tbody></table><figcaption>2021.07–12 · 공통 6개월 · 가격수익률</figcaption></figure>'''
    print_layout = ' print-flow' if p['id'] in ('briefing', 'company') else ''
    projects.append(f'''<section class="project sheet{print_layout}" id="{p['id']}" aria-labelledby="title-{p['id']}">
      <header class="project-header"><span class="chapter">{p['number']}</span><div><p class="eyebrow">{esc(p['category'])}</p><h2 id="title-{p['id']}">{esc(p['title'])}</h2><p class="subtitle">{esc(p['subtitle'])}</p></div></header>
      <p class="project-summary">{esc(p['summary'])}</p>
      <div class="overview-block"><h3>프로젝트 개요</h3><dl class="meta"><div><dt>수행 형태</dt><dd>{esc(p['type'])}</dd></div><div><dt>수행 기간</dt><dd>{esc(p['period'])}</dd></div><div class="wide"><dt>프로젝트 목표</dt><dd>{esc(p['goal'])}</dd></div><div class="wide scope"><dt>검증 범위</dt><dd>{esc(p['scope'])}</dd></div></dl></div>
      <div class="project-columns"><div class="project-main"><div class="text-block"><h3>데이터 및 설계</h3>{lis(p['design'])}</div><div class="text-block"><h3>주요 수행 내용</h3>{lis(p['work'])}</div></div>
      <aside class="results"><p class="result-kicker">검증 결과 및 성과</p><p class="result-metric">{esc(p['metric'])}</p><p class="metric-label">{esc(p['metricLabel'])}</p>{table}{lis(p['results'])}<p class="scope-note">{esc(p['note'])}</p></aside></div>
      <footer class="project-links"><h3>관련 자료</h3>{link('GitHub 저장소',p['repo'],'repo-link')}<div class="evidence-links">{''.join(link(*x) for x in p['links'])}</div></footer>
      <p class="print-folio">김재원 · 이지스자산운용 헤지펀드운용파트 지원 포트폴리오 <span>{int(p['number'])+1:02d} / 05</span></p>
    </section>''')

document = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#142b46"><title>김재원 | 이지스자산운용 지원 포트폴리오</title><meta name="description" content="글로벌 시장 브리핑, 기업분석, 미국 주식 운용자료 관리와 국내 주식 공시자료 분석 경험을 정리한 김재원의 포트폴리오입니다."><link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="styles.css"><script src="app.js" defer></script></head>
<body><a class="skip-link" href="#main">본문으로 이동</a><div class="reading-progress" aria-hidden="true"></div>
<aside class="sidebar"><a href="#overview" class="identity"><span class="identity-label">지원 포트폴리오</span><strong>김재원<span class="identity-dot">.</span></strong><span class="identity-en">JAEWON KIM</span></a><nav aria-label="포트폴리오 목차">{nav}</nav><div class="sidebar-bottom"><p>RESEARCH &amp;<br>OPERATIONS SUPPORT</p><div class="download-links"><a href="igis_hedge_fund_portfolio.pdf" download>PDF 내려받기 ↓</a><a href="igis_hedge_fund_portfolio.md" download>Markdown 원본 ↓</a></div></div></aside>
<main id="main">{profile_page}
{''.join(projects)}<footer class="site-footer"><span>김재원 · 지원 포트폴리오</span><a href="igis_hedge_fund_portfolio.pdf" download>PDF 내려받기 ↓</a><a href="#overview">처음으로 ↑</a></footer></main></body></html>'''
(OUT / 'index.html').write_text(document,encoding='utf-8')
(OUT / '.nojekyll').write_text('',encoding='utf-8')

md = f'# {PROFILE["title"]}\n\n**{DATA["name"]} | {PROFILE["organization"]} {PROFILE["department"]}\n\n'
md += ' / '.join(PROFILE['summary']) + '\n\n## 01. 학력\n\n| 학교 | 전공 | 기간 | 비고 |\n| --- | --- | --- | --- |\n'
md += ''.join('| ' + ' | '.join(e[k] for k in ['school', 'major', 'period', 'status']) + ' |\n' for e in PROFILE['education'])
md += '\n## 02. 교내 활동\n\n'
for a in PROFILE['activities']:
    md += f'### {a["name"]} | {a["period"]}\n\n' + '\n'.join('- '+x for x in a['items']) + '\n\n'
md += '## 03. 자격증 및 수료\n\n| 구분 | 내용 | 취득일 |\n| --- | --- | --- |\n'
md += ''.join(f'| {c["type"]} | {c["name"]} | {c["date"]} |\n' for c in PROFILE['credentials'])
md += f'\n## 04. 실무 경험\n\n**{experience["name"]} | {experience["period"]}**\n\n' + '\n'.join('- '+x for x in experience['items'])
md += '\n\n## 05. 핵심 역량\n\n' + '\n'.join('- '+x for x in PROFILE['competencies'])+'\n\n'
for p in DATA['projects']:
    md += f'---\n\n## [{int(p["number"])}. {p["title"]}]\n\n**프로젝트: {p["subtitle"]}**\n\n### 프로젝트 개요\n\n'
    for label,key in [('수행 형태','type'),('수행 기간','period'),('프로젝트 목표','goal'),('검증 범위','scope')]:
        md += f'- **{label}:** {p[key]}\n'
    for title,key in [('데이터 및 설계','design'),('주요 수행 내용','work'),('검증 결과 및 성과','results')]:
        md += '\n### '+title+'\n\n'+'\n'.join('- '+x for x in p[key])+'\n'
    md += '\n> '+p['note']+'\n\n### 관련 자료\n\n'+f'- [GitHub 저장소]({p["repo"]})\n'+'\n'.join(f'- [{label}]({url})' for label,url in p['links'])+'\n\n'
for path in [ROOT/'igis_hedge_fund_portfolio.md',OUT/'igis_hedge_fund_portfolio.md']:
    path.write_text(md,encoding='utf-8')
print('Generated docs/index.html and Markdown source (4 projects).')
