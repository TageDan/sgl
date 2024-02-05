function drawLine(p1,p2,col,steps){
let x1=p1[0]
let x2=p2[0]
let y1=p1[1]
let y2=p2[1]
let dx=(x2-x1)/steps
let dy=(y2-y1)/steps
let i=0
while(true){
draw(x1+dx*i,y1+dy*i,col)
i=i+1
if(i>steps){
break
}}}
function drawChar(pos,c,col){
let x=pos[0]
let y=pos[1]
let m=[]
if(c=="A"){
m=[[0,1,1,0],[1,0,0,1],[1,1,1,1],[1,0,0,1],[1,0,0,1]]
}if(c=="B"){
m=[[1,1,1,0],[1,0,0,1],[1,1,1,0],[1,0,0,1],[1,1,1,0]]
}if(c=="C"){
m=[[0,1,1,1],[1,0,0,0],[1,0,0,0],[1,0,0,0],[0,1,1,1]]
}if(c=="D"){
m=[[1,1,1,0],[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,1,1,0]]
}if(c=="E"){
m=[[1,1,1,1],[1,0,0,0],[1,1,1,0],[1,0,0,0],[1,1,1,1]]
}if(c=="F"){
m=[[1,1,1,1],[1,0,0,0],[1,1,1,0],[1,0,0,0],[1,0,0,0]]
}if(c=="G"){
m=[[0,1,1,1],[1,0,0,0],[1,0,1,1],[1,0,0,1],[0,1,1,1]]
}if(c=="H"){
m=[[1,0,0,1],[1,0,0,1],[1,1,1,1],[1,0,0,1],[1,0,0,1]]
}if(c=="I"){
m=[[1,1,1],[0,1,0],[0,1,0],[0,1,0],[1,1,1]]
}if(c=="J"){
m=[[0,0,0,1],[0,0,0,1],[0,0,0,1],[1,0,0,1],[0,1,1,0]]
}if(c=="K"){
m=[[1,0,0,1],[1,0,1,0],[1,1,0,0],[1,0,1,0],[1,0,0,1]]
}if(c=="L"){
m=[[1,0,0],[1,0,0],[1,0,0],[1,0,0],[1,1,1]]
}if(c=="M"){
m=[[1,0,0,0,1],[1,1,0,1,1],[1,0,1,0,1],[1,0,0,0,1],[1,0,0,0,1]]
}if(c=="N"){
m=[[1,0,0,1],[1,1,0,1],[1,0,1,1],[1,0,0,1],[1,0,0,1]]
}if(c=="O"){
m=[[0,1,1,0],[1,0,0,1],[1,0,0,1],[1,0,0,1],[0,1,1,0]]
}if(c=="P"){
m=[[1,1,1,0],[1,0,0,1],[1,1,1,0],[1,0,0,0],[1,0,0,0]]
}if(c=="Q"){
m=[[0,1,1,0],[1,0,0,1],[1,0,0,1],[1,0,1,0],[0,1,0,1]]
}if(c=="R"){
m=[[1,1,1,0],[1,0,0,1],[1,1,1,0],[1,0,1,0],[1,0,0,1]]
}if(c=="S"){
m=[[0,1,1,1],[1,0,0,0],[0,1,1,0],[0,0,0,1],[1,1,1,0]]
}if(c=="T"){
m=[[1,1,1],[0,1,0],[0,1,0],[0,1,0],[0,1,0]]
}if(c=="U"){
m=[[1,0,0,1],[1,0,0,1],[1,0,0,1],[1,0,0,1],[0,1,1,0]]
}if(c=="V"){
m=[[1,0,0,0,1],[1,0,0,0,1],[0,1,0,1,0],[0,1,0,1,0],[0,0,1,0,0]]
}if(c=="W"){
m=[[1,0,0,0,1],[1,0,0,0,1],[1,0,1,0,1],[1,1,0,1,1],[1,0,0,0,1]]
}if(c=="X"){
m=[[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,1,0,1,0],[1,0,0,0,1]]
}if(c=="Y"){
m=[[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]]
}if(c=="Z"){
m=[[1,1,1,1],[0,0,0,1],[0,0,1,0],[0,1,0,0],[1,1,1,1]]
}if(c=="."){
m=[[0,0],[0,0],[0,0],[0,0],[1,0]]
}if(c=="!"){
m=[[1],[1],[1],[0],[1]]
}if(c==","){
m=[[0],[0],[0],[1],[1]]
}if(c==" "){
m=[[0,0,0]]
}if(c=="0"){
m=[[0,1,1,0],[1,0,0,1],[1,0,0,1],[1,0,0,1],[0,1,1,0]]
}if(c=="1"){
m=[[0,1],[1,1],[0,1],[0,1],[1,1]]
}if(c=="2"){
m=[[1,1,1],[0,0,1],[0,1,0],[1,0,0],[1,1,1]]
}if(c=="3"){
m=[[1,1,1],[0,0,1],[0,1,1],[0,0,1],[1,1,1]]
}if(c=="4"){
m=[[1,0,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]]
}if(c=="5"){
m=[[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]]
}if(c=="6"){
m=[[0,1,1],[1,0,0],[1,1,1],[1,0,1],[0,1,1]]
}if(c=="7"){
m=[[1,1,1],[0,0,1],[0,1,0],[1,0,0],[1,0,0]]
}if(c=="8"){
m=[[0,1,1,0],[1,0,0,1],[0,1,1,0],[1,0,0,1],[0,1,1,0]]
}if(c=="9"){
m=[[0,1,1],[1,0,1],[0,1,1],[0,0,1],[1,1,0]]
}if(c==":"){
m=[[0],[1],[0],[1],[0]]
}if(c==";"){
m=[[0],[1],[0],[1],[1]]
}let i=(-1)
let w=0
while(true){
i=i+1
if(i==length(m)){
break
}let j=(-1)
while(true){
j=j+1
if(j==length(m[i])){
if(j>w){
w=j
}break
}if(m[i][j]==1){
draw(x+j,y+i,col)
}}}return [x+w+1,y]
}
