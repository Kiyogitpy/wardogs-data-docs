/* CL-516586 sphere/triangle SIMD kernel. Geometry inputs use local UE cm. */
'use strict';
const f=Math.fround;
const sub=(a,b)=>a.map((x,i)=>f(x-b[i]));
const dot=(a,b)=>f(f(f(a[0]*b[0])+f(a[1]*b[1]))+f(a[2]*b[2]));
const cross=(a,b)=>[f(f(a[1]*b[2])-f(a[2]*b[1])),f(f(a[2]*b[0])-f(a[0]*b[2])),f(f(a[0]*b[1])-f(a[1]*b[0]))];
function sphereTriangle(triangle,center,radius){
  const[a,b,c]=triangle.map(p=>p.map(f));center=center.map(f);radius=f(radius);
  const ab=sub(b,a),bc=sub(c,b),ca=sub(a,c),normal=cross(ab,bc);
  const inverse=f(1/f(Math.sqrt(dot(normal,normal))));
  const n=normal.map(x=>f(x*inverse));
  if(Math.abs(dot(n,sub(center,a)))>radius)return false;
  const radiusSquared=f(radius*radius);
  for(const[start,finish,edge]of[[a,b,ab],[b,c,bc],[c,a,ca]]){
    const denominator=dot(edge,edge);
    let t=denominator===0?0:f(dot(sub(center,start),edge)/denominator);
    // MAXPS selects its second operand for an unordered input.
    t=Number.isNaN(t)?0:Math.min(Math.max(t,0),1);
    const closest=start.map((x,i)=>f(f(x*f(1-t))+f(finish[i]*t)));
    const delta=sub(center,closest);
    if(dot(delta,cross(edge,n))>0&&dot(delta,delta)>radiusSquared)return false;
  }
  // Degenerate normals are NaN in this native kernel; unordered edge/plane
  // comparisons do not reject. Candidate BVH bounds are a separate gate.
  return true;
}
function meshSphere(mesh,center,radius,scale=[1,1,1]){
  radius=f(radius);
  // The helper receives translation in unscaled mesh coordinates, then
  // restores mesh scale for the sphere/triangle test and query AABB.
  const scaledCenter=center.map((v,i)=>v*scale[i]);
  const minimum=[],maximum=[];
  for(let i=0;i<3;i++){
    const inverse=1/scale[i],a=(scaledCenter[i]-radius)*inverse,b=(scaledCenter[i]+radius)*inverse;
    minimum.push(f(Math.min(a,b)));maximum.push(f(Math.max(a,b)));
  }
  return meshSphereQuery(mesh,scaledCenter,radius,scale,{min:minimum,max:maximum});
}
// The generic scaled-sphere dispatch supplies a separately transformed AABB.
// Its bounds can admit different faces from the direct sphere overload.
function meshSphereQuery(mesh,center,radius,scale,bounds){
  radius=f(radius);
  const minimum=bounds.min.map(f),maximum=bounds.max.map(f);
  const floatCenter=center.map(f),floatScale=scale.map(f);
  function intersects(lo,hi){
    return lo.every((v,i)=>!(hi[i]<minimum[i]||maximum[i]<v));
  }
  const stack=mesh.bvh.nodes.length?[0]:[],faceOrder=[];
  while(stack.length){
    const node=mesh.bvh.nodes[stack.pop()];
    for(const child of node){
      if(child.childOrFaceIndex===-1||!intersects(child.bounds.min,child.bounds.max))continue;
      if(!child.faceCount)stack.push(child.childOrFaceIndex);
      else for(let face=child.childOrFaceIndex;face<child.childOrFaceIndex+child.faceCount;face++){
        const box=mesh.bvh.faceBounds[face];
        if(!intersects(box.slice(0,3),box.slice(3)))continue;
        faceOrder.push(face);
        const triangle=mesh.triangles[face].map(index=>mesh.vertices[index].map((v,i)=>f(f(v)*floatScale[i])));
        if(sphereTriangle(triangle,floatCenter,radius))return{overlap:true,faceOrder};
      }
    }
  }
  return{overlap:false,faceOrder};
}
function overlapPrefilter(query,shape,component,actors,components,options){
  if(!(query[3]&shape[3]&3)||((query[3]>>>26)&(shape[3]>>>26)))return 0;
  const q=(query[3]>>>21)&31,s=(shape[3]>>>21)&31;
  let result;
  if(query[0]===0)result=query[1]&(1<<s)?(q===0?2:1):0;
  else result=Math.min(shape[1]&(1<<q)?2:shape[2]&(1<<q)?1:0,
    query[1]&(1<<s)?2:query[2]&(1<<s)?1:0);
  if((result===1&&options.ignoreTouches)||(result===2&&options.ignoreBlocks))return 0;
  if(result&&(actors.includes(shape[0])||components.includes(component)))return 0;
  return result===2&&options.demote?1:result;
}
const crossD=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
function rotateD(q,v){
  const t=crossD(q,v).map(x=>2*x),c=crossD(q,t);
  return v.map((x,i)=>(x+q[3]*t[i])+c[i]);
}
function multiplyD(a,b){
  const c=crossD(a,b);
  return [0,1,2].map(i=>a[3]*b[i]+a[i]*b[3]+c[i])
    .concat(a[3]*b[3]-a[0]*b[0]-a[1]*b[1]-a[2]*b[2]);
}
function scaledActorSphereInput(rotation,translation,shapeRotation,shapeTranslation,scale,center,radius){
  rotation=rotation.map(f);radius=f(radius);
  scale=scale.map(x=>{x=f(x);return Math.abs(x)<f(1e-6)?f(1e-6):x;});
  const q=multiplyD(rotation,shapeRotation||[0,0,0,1]);
  const offset=rotateD(rotation,shapeTranslation||[0,0,0]);
  const inverse=q.map((x,i)=>i<3?-x:x);
  const local=rotateD(inverse,center.map((x,i)=>x-(translation[i]+offset[i])));
  const inverseScale=scale.map(x=>f(1/x));
  const restored=local.map((x,i)=>(x*inverseScale[i])*scale[i]);
  const product=scale.map((x,i)=>f(inverseScale[i]*x));
  const extent=product.map(x=>radius*Math.abs(x));
  // The native bounds helper rotates four box diagonals and takes component
  // maxima, rather than summing absolute rotation-matrix terms.
  const diagonals=[1,-1].flatMap(x=>[1,-1].map(z=>rotateD(inverse,[x*extent[0],extent[1],z*extent[2]])));
  const worldExtent=[0,1,2].map(i=>Math.max(...diagonals.map(v=>Math.abs(v[i]))));
  const minimum=[],maximum=[];
  for(let i=0;i<3;i++){
    const a=(restored[i]-worldExtent[i])*(1/scale[i]);
    const b=(restored[i]+worldExtent[i])*(1/scale[i]);
    minimum.push(Math.min(a,b));maximum.push(Math.max(a,b));
  }
  return {center:restored.map(f),radius:f(radius*product[0]),scale,
    bounds:{min:minimum,max:maximum}};
}
function actorSphere(mesh,rotation,translation,shapeRotation,shapeTranslation,scale,center,radius){
  if(scale){
    const input=scaledActorSphereInput(rotation,translation,shapeRotation,shapeTranslation,scale,center,radius);
    return meshSphereQuery(mesh,input.center,input.radius,input.scale,input.bounds);
  }
  rotation=rotation.map(f);
  const q=multiplyD(rotation,shapeRotation||[0,0,0,1]);
  const offset=rotateD(rotation,shapeTranslation||[0,0,0]);
  const inverse=q.map((x,i)=>i<3?-x:x);
  const local=rotateD(inverse,center.map((x,i)=>x-(translation[i]+offset[i])));
  return meshSphere(mesh,local,radius);
}
// Conditional actor loop: supplied bounds/filter state and encounter order.
// Postfilters and active scene membership are supplied outside this model.
function overlapActorShapes(mesh,rotation,translation,shapes,order,query,actors,components,center,radius,options={}){
  const filterCalls=[],shapeVisits=[],touches=[];
  let blocking=false,blockShape=null,continued=true;
  for(const id of order){
    const shape=shapes.find(s=>s.id===id);
    if(shapes.length>1&&center.some((x,i)=>x<shape.bounds.min[i]-radius||x>shape.bounds.max[i]+radius))continue;
    if(components.length&&shape.component_id===undefined)throw new Error('Missing supplied component identity');
    const response=shape.query_enabled?overlapPrefilter(query,shape.filter,shape.component_id,actors,components,options):0;
    filterCalls.push({shape:id,result:response});
    if(!response)continue;
    const hit=actorSphere(shape.mesh||mesh,rotation,translation,shape.rotation,shape.translation,shape.scale,center,radius);
    hit.faceOrder.forEach(face=>shapeVisits.push([id,face]));
    if(!hit.overlap)continue;
    if(response===2||options.anyHit||options.forceBlock){blocking=true;blockShape=id;}
    else touches.push(id);
    if(options.anyHit){continued=false;break;}
  }
  return {filterCalls,shapeVisits,result:{continued,blocking,block_shape:blockShape,touches,
    final:blocking?touches.concat(blockShape):touches.slice()}};
}
function deduplicateOverlapResults(initial,incoming){
  const results=initial.slice(),useHash=initial.length+incoming.length>=3;
  const componentEqual=(a,b)=>(a.index===b.index&&a.serial===b.serial)||(!a.valid&&!b.valid);
  const item=r=>r.component.valid&&r.component.instanced?r.itemIndex:-1;
  const equal=(a,b)=>BigInt(a.physicsOwner)===BigInt(b.physicsOwner)&&item(a)===item(b)&&componentEqual(a.component,b.component);
  const buckets=new Map();
  const half=Math.max(1,(initial.length+incoming.length)>>>1);
  const bucketCount=Math.max(32,2**Math.ceil(Math.log2(half)));
  function hash(row){
    let p=Number((BigInt(row.physicsOwner)>>4n)&0xffffffffn)>>>0;
    p=Math.imul(p^(p>>>16),0x85ebca6b)>>>0;
    p=Math.imul(p^(p>>>13),0xc2b2ae35)>>>0;
    return (p^(p>>>16)^row.component.index^row.component.serial^item(row))&(bucketCount-1);
  }
  function find(row){
    const indices=useHash?(buckets.get(hash(row))||[]):results.map((_,i)=>i);
    return indices.find(i=>equal(results[i],row));
  }
  function bind(row,index){
    const key=hash(row),indices=buckets.get(key)||[];
    const existing=indices.find(i=>equal(results[i],row));
    if(existing!==undefined)indices.splice(indices.indexOf(existing),1);
    indices.unshift(index);buckets.set(key,indices);
  }
  if(useHash)initial.forEach((row,i)=>bind(row,i));
  for(const row of incoming){
    const index=find(row);
    if(index===undefined){results.push(row);if(useHash)bind(row,results.length-1);}
    else if(!results[index].blocking&&row.blocking)results[index]=row;
  }
  return {results,anyBlocking:incoming.some(row=>row.blocking)};
}
module.exports={sphereTriangle,meshSphere,meshSphereQuery,overlapActorShapes,scaledActorSphereInput,actorSphere,deduplicateOverlapResults};
