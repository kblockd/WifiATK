import{a as b}from"./index.2d8c7911.js";import{f as u,d as g,p as r,h,j as e,o as x,a as y,e as D,k as a,w as s,l as v}from"./index.88357001.js";import{I}from"./index.c169b011.js";const k=g({name:"Station",components:{IconRefresh:I},setup(){const t=r([]),n=r([{title:"id",dataIndex:"id",sortable:{sortDirections:["ascend","descend"]}},{title:"bssid",dataIndex:"bssid",sortable:{sortDirections:["ascend","descend"]}},{title:"essid",dataIndex:"essid",sortable:{sortDirections:["ascend","descend"]}},{title:"client",dataIndex:"client",sortable:{sortDirections:["ascend","descend"]}},{title:"first_time",dataIndex:"first_time",sortable:{sortDirections:["ascend","descend"]}},{title:"last_time",dataIndex:"last_time",sortable:{sortDirections:["ascend","descend"]}}]),o=()=>{t.length=0,b.get("manager/api/station/").then(i=>{for(let d of i.data.data)t.push(d)})};return h(async()=>{o()}),{columns:n,tableData:t,getData:o}}}),C={style:{padding:"20px",display:"flex",height:"calc(100% - 40px)"}},w={style:{"background-color":"var(--color-bg-2)","border-radius":"4px",overflow:"auto",width:"100%"}};function $(t,n,o,i,d,B){const c=e("icon-refresh"),l=e("a-button"),p=e("a-typography-title"),_=e("a-divider"),m=e("a-table"),f=e("a-col");return x(),y("div",C,[D("div",w,[a(f,{span:24,style:{padding:"20px 20px 0"}},{default:s(()=>[a(p,{heading:5,style:{"margin-top":"0"}},{default:s(()=>[v(" Station Log "),a(l,{shape:"circle",style:{"margin-left":"20px"},onClick:t.getData},{default:s(()=>[a(c)]),_:1},8,["onClick"])]),_:1}),a(_,{style:{"margin-bottom":"20px","border-bottom":"1px solid rgb(var(--gray-2))"}}),a(m,{columns:t.columns,data:t.tableData},null,8,["columns","data"])]),_:1})])])}const j=u(k,[["render",$]]);export{j as default};
