"""Generate the static GitHub Pages portfolio and editable Markdown."""
from pathlib import Path
import json
import html

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
OUT = ROOT / 'docs'
OUT.mkdir(exist_ok=True)
esc = html.escape

def lis(items):
    return '<ul>' + ''.join('<li>' + esc(x) + '</li>' for x in items) + '</ul>'

def link(label, url, cls=''):
    return f'<a class="{cls}" href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(label)} <span aria-hidden="true">↗</span></a>'

nav = '<a class="nav-link active" href="#overview"><span>00</span>핵심 역량</a>' + ''.join(f'<a class="nav-link" href="#{p["id"]}"><span>{p["number"]}</span>{esc(p["title"].replace(" AI 자동화", "").replace(" 운용 시스템", " 운용자료"))}</a>' for p in DATA['projects'])
projects = []
for p in DATA['projects']:
    table = ''
    if p['id'] == 'vfs':
        table = '''<figure class="result-table"><table><caption>VFS−Value 월평균 차이</caption><thead><tr><th scope="col">가중 방식</th><th scope="col">상대성과</th></tr></thead><tbody><tr><th scope="row">시가총액가중</th><td>+0.43%p</td></tr><tr><th scope="row">동일가중</th><td>−0.4158%p</td></tr></tbody></table><figcaption>2021.07–12 · 공통 6개월 · 가격수익률</figcaption></figure>'''
    projects.append(f'''<section class="project sheet" id="{p['id']}" aria-labelledby="title-{p['id']}">
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
<aside class="sidebar"><a href="#overview" class="identity"><span class="identity-label">지원 포트폴리오</span><strong>김재원<span class="identity-dot">.</span></strong><span class="identity-en">JAEWON KIM</span></a><nav aria-label="포트폴리오 목차">{nav}</nav><div class="sidebar-bottom"><p>RESEARCH &amp;<br>OPERATIONS SUPPORT</p><a href="igis_hedge_fund_portfolio.md" download>Markdown 원본 ↓</a></div></aside>
<main id="main"><section class="cover sheet" id="overview" aria-labelledby="cover-title"><header class="cover-meta"><span>이지스자산운용</span><span>증권부문 헤지펀드운용파트</span></header><div class="cover-heading"><p class="eyebrow">경력기술서형 포트폴리오</p><h1 id="cover-title">시장 리서치에서<br>운용자료 관리까지</h1><p class="cover-description">글로벌 시장 브리핑과 기업자료 검증 경험을 바탕으로<br class="desktop-break"> 주식 리서치와 운용지원에 필요한 작업을 정리했습니다.</p></div>
<div class="competencies"><div class="competency"><span class="skill-number">01</span><div><h2>시장 및 기업 리서치</h2><p>글로벌 시장 브리핑 작성과 해외 IB 리서치 분석<br>기업 공시 대조 및 국내 주식 종목선별 전략 실증</p></div><span class="skill-tag">자료 수집과 해석</span></div><div class="competency"><span class="skill-number">02</span><div><h2>운용자료 관리</h2><p>미국 대형주 목표 비중과 기존 보유분 비교<br>주문 티켓 생성 및 Excel 원장 7개 시트 연계</p></div><span class="skill-tag">주문자료와 원장</span></div><div class="competency"><span class="skill-number">03</span><div><h2>AI 기반 업무 효율화</h2><p>시장 브리핑의 반복 검증 업무 자동화<br>공시와 실적발표를 대조하는 기업분석 AI 스킬 개발</p></div><span class="skill-tag">반복 업무 개선</span></div></div>
<div class="contents"><h2>프로젝트 살펴보기</h2><div class="contents-grid">{''.join(f'<a href="#{p["id"]}"><span>{p["number"]}</span><strong>{esc(p["title"])}</strong><span aria-hidden="true">↗</span></a>' for p in DATA['projects'])}</div></div><p class="cover-note">학회 활동과 개인 프로젝트를 바탕으로 작성했습니다.<br>각 프로젝트의 수행 범위와 검증 한계는 본문에 함께 표시했습니다.</p><p class="print-folio">김재원 · 이지스자산운용 헤지펀드운용파트 지원 포트폴리오 <span>01 / 05</span></p></section>
{''.join(projects)}<footer class="site-footer"><span>김재원 · 지원 포트폴리오</span><a href="#overview">처음으로 ↑</a></footer></main></body></html>'''
(OUT / 'index.html').write_text(document,encoding='utf-8')
(OUT / '.nojekyll').write_text('',encoding='utf-8')

md = '# 이지스자산운용 헤지펀드운용파트 지원 포트폴리오\n\n김재원\n\n## 핵심 역량 요약\n\n'
md += '- **시장 및 기업 리서치:** 글로벌 시장 브리핑 작성과 해외 IB 리서치 분석. 기업 공시 대조 및 국내 주식 종목선별 전략 실증\n- **운용자료 관리:** 미국 대형주 목표 비중과 보유분 비교. 주문 티켓 생성 및 Excel 원장 7개 시트 연계\n- **AI 활용:** 시장 브리핑 반복 검증 자동화. 공시와 실적발표를 대조하는 기업분석 AI 스킬 개발\n\n'
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
