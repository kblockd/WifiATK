import{a as b}from"./index.5bfded66.js";import{f as h,d as u,p as c,h as x,j as t,o as g,a as y,e as D,k as a,w as n,l as I}from"./index.c7bb5816.js";import{I as v}from"./index.02075c8f.js";const w=u({name:"Wifi",components:{IconRefresh:v},setup(){const e=c([]),i=c([{title:"id",dataIndex:"id",sortable:{sortDirections:["ascend","descend"]}},{title:"bssid",dataIndex:"bssid",sortable:{sortDirections:["ascend","descend"]}},{title:"essid",dataIndex:"essid",sortable:{sortDirections:["ascend","descend"]}},{title:"channel",dataIndex:"channel",sortable:{sortDirections:["ascend","descend"]}},{title:"privacy",dataIndex:"privacy",sortable:{sortDirections:["ascend","descend"]}},{title:"cipher",dataIndex:"cipher",sortable:{sortDirections:["ascend","descend"]}},{title:"authentication",dataIndex:"authentication",sortable:{sortDirections:["ascend","descend"]}},{title:"power",dataIndex:"power",sortable:{sortDirections:["ascend","descend"]}},{title:"first_time",dataIndex:"first_time",sortable:{sortDirections:["ascend","descend"]}},{title:"last_time",dataIndex:"last_time",sortable:{sortDirections:["ascend","descend"]}}]),o=()=>{e.length=0,b.get("../api/wifi/").then(s=>{for(let d of s.data.data)e.push(d),console.log(s.data)})};return x(async()=>{o()}),{columns:i,tableData:e,getData:o}}}),k={style:{padding:"20px",display:"flex",height:"calc(100% - 40px)"}},C={style:{"background-color":"var(--color-bg-2)","border-radius":"4px",overflow:"auto",width:"100%"}};function $(e,i,o,s,d,B){const r=t("icon-refresh"),l=t("a-button"),p=t("a-typography-title"),_=t("a-divider"),m=t("a-table"),f=t("a-col");return g(),y("div",k,[D("div",C,[a(f,{span:24,style:{padding:"20px 20px 0"}},{default:n(()=>[a(p,{heading:5,style:{"margin-top":"0"}},{default:n(()=>[I(" Wifi Log "),a(l,{shape:"circle",style:{"margin-left":"20px"},onClick:e.getData},{default:n(()=>[a(r)]),_:1},8,["onClick"])]),_:1}),a(_,{style:{"margin-bottom":"20px","border-bottom":"1px solid rgb(var(--gray-2))"}}),a(m,{columns:e.columns,data:e.tableData},null,8,["columns","data"])]),_:1})])])}const j=h(w,[["render",$]]);export{j as default};
