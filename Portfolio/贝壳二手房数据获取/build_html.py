import json

with open(r'd:\day24个人作品集搭建+简历优化\day24个人作品集搭建+简历优化\02课程代码\01个人作品集部署\01个人作品集\Portfolio\贝壳二手房数据获取\beike_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

data_json = json.dumps(data, ensure_ascii=False)

html = r'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>贝壳二手房数据分析看板</title>
<script src="echarts.min.js"></script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg: #0a0a0f;
    --bg2: #11111a;
    --panel: rgba(20, 20, 30, 0.72);
    --panel-border: rgba(212, 175, 55, 0.25);
    --gold: #d4af37;
    --gold-light: #f0d98a;
    --gold-soft: rgba(212, 175, 55, 0.14);
    --text: #e8e6df;
    --text-dim: #9a9688;
    --text-faint: #5c5850;
    --red: #e8554e;
    --green: #4ade80;
  }
  html, body { min-height: 100vh; }
  body {
    font-family: "PingFang SC", "Microsoft YaHei", -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text);
    overflow-x: hidden;
    position: relative;
  }
  body::before {
    content: '';
    position: fixed; inset: 0; z-index: 0; pointer-events: none;
    background:
      radial-gradient(ellipse 800px 500px at 15% 10%, rgba(212,175,55,0.10), transparent 60%),
      radial-gradient(ellipse 700px 500px at 85% 20%, rgba(180,140,40,0.08), transparent 60%),
      radial-gradient(ellipse 900px 600px at 50% 100%, rgba(212,175,55,0.06), transparent 70%);
  }
  .wrap { position: relative; z-index: 1; max-width: 1500px; margin: 0 auto; padding: 24px 28px 60px; }

  /* Header */
  header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 18px 26px; margin-bottom: 22px;
    background: linear-gradient(135deg, rgba(212,175,55,0.10), rgba(20,20,30,0.6));
    border: 1px solid var(--panel-border);
    border-radius: 14px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4), inset 0 1px 0 rgba(212,175,55,0.2);
  }
  .header-left h1 {
    font-size: 26px; font-weight: 700; letter-spacing: 2px;
    background: linear-gradient(90deg, var(--gold-light), var(--gold));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  }
  .header-left p { color: var(--text-dim); font-size: 13px; margin-top: 4px; letter-spacing: 1px; }
  .header-right { text-align: right; }
  .header-right .city { font-size: 15px; color: var(--gold-light); font-weight: 600; }
  .header-right .date { font-size: 12px; color: var(--text-dim); margin-top: 3px; }

  /* Stat cards */
  .stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; margin-bottom: 22px; }
  .stat-card {
    background: var(--panel); border: 1px solid var(--panel-border); border-radius: 12px;
    padding: 20px 22px; position: relative; overflow: hidden;
    backdrop-filter: blur(10px);
    transition: transform .25s, border-color .25s;
  }
  .stat-card:hover { transform: translateY(-3px); border-color: var(--gold); }
  .stat-card::after {
    content: ''; position: absolute; top: 0; right: 0; width: 60px; height: 60px;
    background: radial-gradient(circle, var(--gold-soft), transparent 70%);
  }
  .stat-label { color: var(--text-dim); font-size: 13px; letter-spacing: 1px; }
  .stat-value {
    font-size: 32px; font-weight: 700; margin-top: 8px;
    color: var(--gold-light); font-family: "DIN Alternate", "Arial", sans-serif;
  }
  .stat-unit { font-size: 14px; color: var(--text-dim); font-weight: 400; margin-left: 4px; }
  .stat-sub { font-size: 12px; color: var(--text-faint); margin-top: 6px; }

  /* Filter bar */
  .filter-bar {
    display: flex; flex-wrap: wrap; gap: 12px; align-items: center;
    background: var(--panel); border: 1px solid var(--panel-border); border-radius: 12px;
    padding: 14px 18px; margin-bottom: 22px; backdrop-filter: blur(10px);
  }
  .filter-bar label { color: var(--text-dim); font-size: 13px; margin-right: 4px; }
  .filter-bar input, .filter-bar select {
    background: rgba(0,0,0,0.35); border: 1px solid rgba(212,175,55,0.3); color: var(--text);
    padding: 7px 12px; border-radius: 7px; font-size: 13px; outline: none;
    transition: border-color .2s;
  }
  .filter-bar input:focus, .filter-bar select:focus { border-color: var(--gold); }
  .filter-bar .search { flex: 1; min-width: 200px; }
  .filter-bar .reset-btn {
    background: transparent; border: 1px solid var(--gold); color: var(--gold);
    padding: 7px 16px; border-radius: 7px; cursor: pointer; font-size: 13px;
    transition: all .2s;
  }
  .filter-bar .reset-btn:hover { background: var(--gold); color: #0a0a0f; }

  /* Charts grid */
  .charts { display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px; margin-bottom: 22px; }
  .chart-card {
    background: var(--panel); border: 1px solid var(--panel-border); border-radius: 12px;
    padding: 16px 18px; backdrop-filter: blur(10px);
  }
  .chart-card.full { grid-column: span 2; }
  .chart-title {
    font-size: 14px; font-weight: 600; color: var(--gold-light); margin-bottom: 10px;
    padding-left: 10px; border-left: 3px solid var(--gold); letter-spacing: 1px;
  }
  .chart-box { width: 100%; height: 320px; }
  .chart-card.full .chart-box { height: 380px; }

  /* Table */
  .table-card {
    background: var(--panel); border: 1px solid var(--panel-border); border-radius: 12px;
    padding: 16px 18px; backdrop-filter: blur(10px);
  }
  .table-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
  .table-head .result-count { color: var(--text-dim); font-size: 13px; }
  .table-head .result-count b { color: var(--gold-light); }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  thead th {
    text-align: left; padding: 11px 10px; color: var(--gold);
    border-bottom: 1px solid var(--panel-border); font-weight: 600; letter-spacing: 0.5px;
    position: sticky; top: 0; background: rgba(20,20,30,0.95); cursor: pointer; user-select: none;
  }
  thead th:hover { color: var(--gold-light); }
  thead th .arrow { font-size: 10px; color: var(--text-faint); margin-left: 4px; }
  tbody td { padding: 10px; border-bottom: 1px solid rgba(212,175,55,0.08); }
  tbody tr { transition: background .15s; }
  tbody tr:hover { background: var(--gold-soft); }
  .price-total { color: var(--gold-light); font-weight: 700; font-family: "DIN Alternate", Arial, sans-serif; }
  .price-unit { color: var(--text-dim); }
  .addr { color: var(--text); }
  .title-cell { max-width: 260px; }
  .title-cell a { color: var(--text); text-decoration: none; }
  .title-cell a:hover { color: var(--gold-light); text-decoration: underline; }
  .tag {
    display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px;
    background: var(--gold-soft); color: var(--gold-light); border: 1px solid rgba(212,175,55,0.3);
    margin-right: 4px;
  }
  .pagination { display: flex; justify-content: center; align-items: center; gap: 8px; margin-top: 16px; }
  .pagination button {
    background: rgba(0,0,0,0.3); border: 1px solid var(--panel-border); color: var(--text);
    padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 13px; transition: all .2s;
  }
  .pagination button:hover:not(:disabled) { border-color: var(--gold); color: var(--gold-light); }
  .pagination button:disabled { opacity: 0.4; cursor: not-allowed; }
  .pagination .page-info { color: var(--text-dim); font-size: 13px; padding: 0 8px; }
  .pagination .active { background: var(--gold); color: #0a0a0f; border-color: var(--gold); }

  .scroll-wrap { max-height: 560px; overflow-y: auto; }
  .scroll-wrap::-webkit-scrollbar { width: 8px; }
  .scroll-wrap::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); }
  .scroll-wrap::-webkit-scrollbar-thumb { background: rgba(212,175,55,0.3); border-radius: 4px; }
  .scroll-wrap::-webkit-scrollbar-thumb:hover { background: rgba(212,175,55,0.5); }

  @media (max-width: 900px) {
    .stats { grid-template-columns: repeat(2, 1fr); }
    .charts { grid-template-columns: 1fr; }
    .chart-card.full { grid-column: span 1; }
  }
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div class="header-left">
      <h1>贝壳二手房数据分析看板</h1>
      <p>KE.COM · 二手房市场数据可视化分析</p>
    </div>
    <div class="header-right">
      <div class="city">成都 · Chengdu</div>
      <div class="date">数据更新：2026-10</div>
    </div>
  </header>

  <div class="stats" id="stats"></div>

  <div class="filter-bar">
    <input type="text" id="search" class="search" placeholder="搜索标题 / 小区地址...">
    <label>户型</label>
    <select id="f-rooms"><option value="">全部</option></select>
    <label>楼层</label>
    <select id="f-floor">
      <option value="">全部</option><option value="高楼层">高楼层</option>
      <option value="中楼层">中楼层</option><option value="低楼层">低楼层</option>
    </select>
    <label>总价(万)</label>
    <input type="number" id="f-min" placeholder="最低" style="width:80px"> -
    <input type="number" id="f-max" placeholder="最高" style="width:80px">
    <button class="reset-btn" id="reset">重置</button>
  </div>

  <div class="charts">
    <div class="chart-card"><div class="chart-title">总价分布（万元）</div><div class="chart-box" id="c1"></div></div>
    <div class="chart-card"><div class="chart-title">单价分布（元/㎡）</div><div class="chart-box" id="c2"></div></div>
    <div class="chart-card"><div class="chart-title">户型分布</div><div class="chart-box" id="c3"></div></div>
    <div class="chart-card"><div class="chart-title">楼层占比</div><div class="chart-box" id="c4"></div></div>
    <div class="chart-card"><div class="chart-title">朝向分布 Top10</div><div class="chart-box" id="c5"></div></div>
    <div class="chart-card full"><div class="chart-title">面积 vs 总价 散点图</div><div class="chart-box" id="c6"></div></div>
  </div>

  <div class="table-card">
    <div class="table-head">
      <div class="chart-title" style="margin:0;border:none;padding:0;">房源明细</div>
      <div class="result-count">共 <b id="rcount">0</b> 条房源</div>
    </div>
    <div class="scroll-wrap">
      <table>
        <thead>
          <tr>
            <th data-k="title">标题<span class="arrow">↕</span></th>
            <th data-k="addr">小区</th>
            <th data-k="rooms">户型</th>
            <th data-k="area">面积(㎡)</th>
            <th data-k="floor">楼层</th>
            <th data-k="orient">朝向</th>
            <th data-k="total">总价(万)<span class="arrow">↕</span></th>
            <th data-k="unit">单价(元/㎡)</th>
          </tr>
        </thead>
        <tbody id="tbody"></tbody>
      </table>
    </div>
    <div class="pagination" id="pagination"></div>
  </div>
</div>

<script>
const RAW = ''' + data_json + r''';

const gold = ['#d4af37','#f0d98a','#b8941f','#e8c865','#8a6d14','#c9a227'];
const baseAxis = { axisLine:{lineStyle:{color:'rgba(212,175,55,0.3)'}}, axisLabel:{color:'#9a9688'}, splitLine:{lineStyle:{color:'rgba(212,175,55,0.08)'}} };

let state = { data: RAW.slice(), sort: {k:'total', d:'desc'}, page:1, size:15 };

function fmt(n){ return Number(n).toLocaleString('zh-CN'); }

function calcStats(arr){
  const n = arr.length;
  const tot = arr.map(d=>d.total);
  const unit = arr.map(d=>d.unit);
  const area = arr.map(d=>d.area).filter(Boolean);
  return {
    count: n,
    avgTotal: n? (tot.reduce((a,b)=>a+b,0)/n) : 0,
    avgUnit: n? (unit.reduce((a,b)=>a+b,0)/n) : 0,
    avgArea: area.length? (area.reduce((a,b)=>a+b,0)/area.length) : 0,
    maxTotal: n? Math.max(...tot) : 0,
    minTotal: n? Math.min(...tot) : 0,
  };
}

function renderStats(s){
  const cards = [
    {l:'房源总数', v:fmt(s.count), u:'套', sub:`总价区间 ${fmt(s.minTotal)} - ${fmt(s.maxTotal)} 万`},
    {l:'平均总价', v:s.avgTotal.toFixed(1), u:'万', sub:`单价均值 ${fmt(Math.round(s.avgUnit))} 元/㎡`},
    {l:'平均单价', v:fmt(Math.round(s.avgUnit)), u:'元/㎡', sub:`每平米均价`},
    {l:'平均面积', v:s.avgArea.toFixed(1), u:'㎡', sub:`单套建筑面积均值`},
  ];
  document.getElementById('stats').innerHTML = cards.map(c=>`
    <div class="stat-card">
      <div class="stat-label">${c.l}</div>
      <div class="stat-value">${c.v}<span class="stat-unit">${c.u}</span></div>
      <div class="stat-sub">${c.sub}</div>
    </div>`).join('');
}

function hist(arr, bins, min, max){
  const step = (max-min)/bins;
  const counts = new Array(bins).fill(0);
  const labels = [];
  for(let i=0;i<bins;i++){ labels.push((min+step*i).toFixed(0)); }
  arr.forEach(v=>{
    let idx = Math.floor((v-min)/step);
    if(idx<0) idx=0; if(idx>=bins) idx=bins-1;
    counts[idx]++;
  });
  return {labels, counts};
}

function chart1(arr){
  const vals = arr.map(d=>d.total).filter(v=>v<400);
  const h = hist(vals, 16, 0, 400);
  echarts.init(document.getElementById('c1')).setOption({
    tooltip:{trigger:'axis', backgroundColor:'rgba(10,10,15,0.92)', borderColor:'#d4af37', textStyle:{color:'#e8e6df'}},
    grid:{left:50,right:20,top:20,bottom:40},
    xAxis:{type:'category', data:h.labels, ...baseAxis, name:'万元', nameTextStyle:{color:'#9a9688'}},
    yAxis:{type:'value', ...baseAxis},
    series:[{type:'bar', data:h.counts, itemStyle:{color:{type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'#f0d98a'},{offset:1,color:'#8a6d14'}]}, borderRadius:[4,4,0,0]}}]
  });
}

function chart2(arr){
  const vals = arr.map(d=>d.unit).filter(v=>v<40000);
  const h = hist(vals, 16, 0, 40000);
  echarts.init(document.getElementById('c2')).setOption({
    tooltip:{trigger:'axis', backgroundColor:'rgba(10,10,15,0.92)', borderColor:'#d4af37', textStyle:{color:'#e8e6df'}},
    grid:{left:55,right:20,top:20,bottom:40},
    xAxis:{type:'category', data:h.labels, ...baseAxis, name:'元/㎡', nameTextStyle:{color:'#9a9688'}},
    yAxis:{type:'value', ...baseAxis},
    series:[{type:'bar', data:h.counts, itemStyle:{color:{type:'linear',x:0,y:0,x2:0,y2:1,colorStops:[{offset:0,color:'#e8c865'},{offset:1,color:'#b8941f'}]}, borderRadius:[4,4,0,0]}}]
  });
}

function chart3(arr){
  const m = {};
  arr.forEach(d=>{ if(d.rooms) m[d.rooms]=(m[d.rooms]||0)+1; });
  const entries = Object.entries(m).sort((a,b)=>b[1]-a[1]).slice(0,10);
  echarts.init(document.getElementById('c3')).setOption({
    tooltip:{trigger:'axis', backgroundColor:'rgba(10,10,15,0.92)', borderColor:'#d4af37', textStyle:{color:'#e8e6df'}},
    grid:{left:50,right:20,top:20,bottom:40},
    xAxis:{type:'category', data:entries.map(e=>e[0]), ...baseAxis},
    yAxis:{type:'value', ...baseAxis},
    series:[{type:'bar', data:entries.map(e=>e[1]), itemStyle:{color:'#d4af37', borderRadius:[4,4,0,0]}, label:{show:true,position:'top',color:'#f0d98a',fontSize:11}}]
  });
}

function chart4(arr){
  const m = {};
  arr.forEach(d=>{ if(d.floor) m[d.floor]=(m[d.floor]||0)+1; });
  const data = Object.entries(m).map(([n,v])=>({name:n,value:v}));
  echarts.init(document.getElementById('c4')).setOption({
    tooltip:{trigger:'item', backgroundColor:'rgba(10,10,15,0.92)', borderColor:'#d4af37', textStyle:{color:'#e8e6df'}, formatter:'{b}: {c} ({d}%)'},
    legend:{bottom:0, textStyle:{color:'#9a9688'}},
    series:[{type:'pie', radius:['42%','68%'], center:['50%','45%'], data,
      itemStyle:{borderColor:'#0a0a0f', borderWidth:2},
      label:{color:'#e8e6df', formatter:'{b}\n{d}%'},
      color: gold
    }]
  });
}

function chart5(arr){
  const m = {};
  arr.forEach(d=>{ if(d.orient) m[d.orient]=(m[d.orient]||0)+1; });
  const entries = Object.entries(m).sort((a,b)=>b[1]-a[1]).slice(0,10).reverse();
  echarts.init(document.getElementById('c5')).setOption({
    tooltip:{trigger:'axis', backgroundColor:'rgba(10,10,15,0.92)', borderColor:'#d4af37', textStyle:{color:'#e8e6df'}},
    grid:{left:70,right:30,top:20,bottom:30},
    xAxis:{type:'value', ...baseAxis},
    yAxis:{type:'category', data:entries.map(e=>e[0]), ...baseAxis},
    series:[{type:'bar', data:entries.map(e=>e[1]), itemStyle:{color:{type:'linear',x:0,y:0,x2:1,y2:0,colorStops:[{offset:0,color:'#8a6d14'},{offset:1,color:'#f0d98a'}]}, borderRadius:[0,4,4,0]}, label:{show:true,position:'right',color:'#f0d98a',fontSize:11}}]
  });
}

function chart6(arr){
  const data = arr.filter(d=>d.area && d.total).map(d=>[d.area, d.total, d.title]);
  echarts.init(document.getElementById('c6')).setOption({
    tooltip:{trigger:'item', backgroundColor:'rgba(10,10,15,0.92)', borderColor:'#d4af37', textStyle:{color:'#e8e6df'},
      formatter:p=>`${p.data[2]}<br/>面积: ${p.data[0]} ㎡<br/>总价: ${p.data[1]} 万`},
    grid:{left:60,right:30,top:20,bottom:50},
    xAxis:{type:'value', name:'面积(㎡)', ...baseAxis, nameTextStyle:{color:'#9a9688'}},
    yAxis:{type:'value', name:'总价(万)', ...baseAxis, nameTextStyle:{color:'#9a9688'}},
    series:[{type:'scatter', data, symbolSize:7, itemStyle:{color:'rgba(212,175,55,0.55)', borderColor:'#d4af37', borderWidth:0.5}}]
  });
}

function renderCharts(arr){
  chart1(arr); chart2(arr); chart3(arr); chart4(arr); chart5(arr); chart6(arr);
}

function applyFilter(){
  const kw = document.getElementById('search').value.trim().toLowerCase();
  const rooms = document.getElementById('f-rooms').value;
  const floor = document.getElementById('f-floor').value;
  const min = parseFloat(document.getElementById('f-min').value);
  const max = parseFloat(document.getElementById('f-max').value);
  state.data = RAW.filter(d=>{
    if(kw && !(d.title.toLowerCase().includes(kw) || (d.addr||'').toLowerCase().includes(kw))) return false;
    if(rooms && d.rooms!==rooms) return false;
    if(floor && d.floor!==floor) return false;
    if(!isNaN(min) && d.total<min) return false;
    if(!isNaN(max) && d.total>max) return false;
    return true;
  });
  state.page = 1;
  refresh();
}

function refresh(){
  renderStats(calcStats(state.data));
  renderCharts(state.data);
  renderTable();
}

function renderTable(){
  let arr = state.data.slice();
  const {k,d} = state.sort;
  arr.sort((a,b)=>{
    let va=a[k], vb=b[k];
    if(typeof va==='string'){ return d==='asc'? va.localeCompare(vb,'zh') : vb.localeCompare(va,'zh'); }
    return d==='asc'? (va||0)-(vb||0) : (vb||0)-(va||0);
  });
  document.getElementById('rcount').textContent = arr.length;
  const total = Math.ceil(arr.length/state.size) || 1;
  if(state.page>total) state.page = total;
  const start = (state.page-1)*state.size;
  const pageData = arr.slice(start, start+state.size);
  document.getElementById('tbody').innerHTML = pageData.map(d=>`
    <tr>
      <td class="title-cell"><a href="${d.url}" target="_blank" rel="noopener">${d.title}</a></td>
      <td class="addr">${d.addr||''}</td>
      <td>${d.rooms? `<span class="tag">${d.rooms}</span>`:''}</td>
      <td>${d.area? d.area.toFixed(1):''}</td>
      <td>${d.floor||''}</td>
      <td>${d.orient||''}</td>
      <td class="price-total">${d.total.toFixed(1)}</td>
      <td class="price-unit">${fmt(Math.round(d.unit))}</td>
    </tr>`).join('');
  renderPagination(total);
}

function renderPagination(total){
  const el = document.getElementById('pagination');
  let html = `<button ${state.page<=1?'disabled':''} onclick="goPage(${state.page-1})">上一页</button>`;
  const maxShow = 7;
  let s = Math.max(1, state.page - 3), e = Math.min(total, s + maxShow - 1);
  s = Math.max(1, e - maxShow + 1);
  for(let i=s;i<=e;i++){
    html += `<button class="${i===state.page?'active':''}" onclick="goPage(${i})">${i}</button>`;
  }
  html += `<span class="page-info">${state.page} / ${total}</span>`;
  html += `<button ${state.page>=total?'disabled':''} onclick="goPage(${state.page+1})">下一页</button>`;
  el.innerHTML = html;
}

function goPage(p){ state.page = p; renderTable(); window.scrollTo({top:document.querySelector('.table-card').offsetTop-20, behavior:'smooth'}); }

function populateRooms(){
  const m = {};
  RAW.forEach(d=>{ if(d.rooms) m[d.rooms]=1; });
  const sel = document.getElementById('f-rooms');
  Object.keys(m).sort().forEach(r=>{ const o=document.createElement('option'); o.value=r; o.textContent=r; sel.appendChild(o); });
}

document.getElementById('search').addEventListener('input', applyFilter);
document.getElementById('f-rooms').addEventListener('change', applyFilter);
document.getElementById('f-floor').addEventListener('change', applyFilter);
document.getElementById('f-min').addEventListener('input', applyFilter);
document.getElementById('f-max').addEventListener('input', applyFilter);
document.getElementById('reset').addEventListener('click', ()=>{
  document.getElementById('search').value='';
  document.getElementById('f-rooms').value='';
  document.getElementById('f-floor').value='';
  document.getElementById('f-min').value='';
  document.getElementById('f-max').value='';
  applyFilter();
});
document.querySelectorAll('thead th[data-k]').forEach(th=>{
  th.addEventListener('click', ()=>{
    const k = th.dataset.k;
    if(state.sort.k===k){ state.sort.d = state.sort.d==='asc'?'desc':'asc'; }
    else { state.sort.k=k; state.sort.d='asc'; }
    renderTable();
  });
});
window.addEventListener('resize', ()=>{
  ['c1','c2','c3','c4','c5','c6'].forEach(id=>{ const c=echarts.getInstanceByDom(document.getElementById(id)); if(c) c.resize(); });
});

populateRooms();
refresh();
</script>
</body>
</html>'''

out = r'd:\day24个人作品集搭建+简历优化\day24个人作品集搭建+简历优化\02课程代码\01个人作品集部署\01个人作品集\Portfolio\贝壳二手房数据获取\贝壳二手房数据看板.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print('HTML written:', out)
print('Size:', round(len(html)/1024, 1), 'KB')
