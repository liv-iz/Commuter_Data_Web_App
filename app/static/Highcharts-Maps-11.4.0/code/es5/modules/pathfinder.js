!/**
 * Highcharts Gantt JS v11.4.0 (2024-03-04)
 *
 * Pathfinder
 *
 * (c) 2016-2024 Øystein Moseng
 *
 * License: www.highcharts.com/license
 */function(t){"object"==typeof module&&module.exports?(t.default=t,module.exports=t):"function"==typeof define&&define.amd?define("highcharts/modules/pathfinder",["highcharts"],function(n){return t(n),t.Highcharts=n,t}):t("undefined"!=typeof Highcharts?Highcharts:void 0)}(function(t){"use strict";var n=t?t._modules:{};function i(t,n,i,r){t.hasOwnProperty(n)||(t[n]=r.apply(null,i),"function"==typeof CustomEvent&&window.dispatchEvent(new CustomEvent("HighchartsModuleLoaded",{detail:{path:n,module:t[n]}})))}i(n,"Gantt/Connection.js",[n["Core/Globals.js"],n["Core/Utilities.js"]],function(t,n){var i=n.defined,r=n.error,e=n.merge,a=n.objectEach,o=t.deg2rad,s=Math.max,h=Math.min;return function(){function t(t,n,i){this.init(t,n,i)}return t.prototype.init=function(t,n,i){this.fromPoint=t,this.toPoint=n,this.options=i,this.chart=t.series.chart,this.pathfinder=this.chart.pathfinder},t.prototype.renderPath=function(t,n){var i=this.chart,r=i.styledMode,e=this.pathfinder,a={},o=this.graphics&&this.graphics.path;e.group||(e.group=i.renderer.g().addClass("highcharts-pathfinder-group").attr({zIndex:-1}).add(i.seriesGroup)),e.group.translate(i.plotLeft,i.plotTop),o&&o.renderer||(o=i.renderer.path().add(e.group),r||o.attr({opacity:0})),o.attr(n),a.d=t,r||(a.opacity=1),o.animate(a),this.graphics=this.graphics||{},this.graphics.path=o},t.prototype.addMarker=function(t,n,i){var r,e,a,s,h,c,x,d,M=this.fromPoint.series.chart,l=M.pathfinder,p=M.renderer,f="start"===t?this.fromPoint:this.toPoint,y=f.getPathfinderAnchorPoint(n);n.enabled&&((d="start"===t?i[1]:i[i.length-2])&&"M"===d[0]||"L"===d[0])&&(x={x:d[1],y:d[2]},e=f.getRadiansToVector(x,y),r=f.getMarkerVector(e,n.radius,y),a=-e/o,n.width&&n.height?(h=n.width,c=n.height):h=c=2*n.radius,this.graphics=this.graphics||{},s={x:r.x-h/2,y:r.y-c/2,width:h,height:c,rotation:a,rotationOriginX:r.x,rotationOriginY:r.y},this.graphics[t]?this.graphics[t].animate(s):(this.graphics[t]=p.symbol(n.symbol).addClass("highcharts-point-connecting-path-"+t+"-marker highcharts-color-"+this.fromPoint.colorIndex).attr(s).add(l.group),p.styledMode||this.graphics[t].attr({fill:n.color||this.fromPoint.color,stroke:n.lineColor,"stroke-width":n.lineWidth,opacity:0}).animate({opacity:1},f.series.options.animation)))},t.prototype.getPath=function(t){var n=this.pathfinder,i=this.chart,a=n.algorithms[t.type],o=n.chartObstacles;return"function"!=typeof a?(r('"'+t.type+'" is not a Pathfinder algorithm.'),{path:[],obstacles:[]}):(a.requiresObstacles&&!o&&(o=n.chartObstacles=n.getChartObstacles(t),i.options.connectors.algorithmMargin=t.algorithmMargin,n.chartObstacleMetrics=n.getObstacleMetrics(o)),a(this.fromPoint.getPathfinderAnchorPoint(t.startMarker),this.toPoint.getPathfinderAnchorPoint(t.endMarker),e({chartObstacles:o,lineObstacles:n.lineObstacles||[],obstacleMetrics:n.chartObstacleMetrics,hardBounds:{xMin:0,xMax:i.plotWidth,yMin:0,yMax:i.plotHeight},obstacleOptions:{margin:t.algorithmMargin},startDirectionX:n.getAlgorithmStartDirection(t.startMarker)},t)))},t.prototype.render=function(){var t=this.fromPoint,n=t.series,r=n.chart,a=r.pathfinder,o={},c=e(r.options.connectors,n.options.connectors,t.options.connectors,this.options);!r.styledMode&&(o.stroke=c.lineColor||t.color,o["stroke-width"]=c.lineWidth,c.dashStyle&&(o.dashstyle=c.dashStyle)),o.class="highcharts-point-connecting-path highcharts-color-"+t.colorIndex,i((c=e(o,c)).marker.radius)||(c.marker.radius=h(s(Math.ceil((c.algorithmMargin||8)/2)-1,1),5));var x=this.getPath(c),d=x.path;x.obstacles&&(a.lineObstacles=a.lineObstacles||[],a.lineObstacles=a.lineObstacles.concat(x.obstacles)),this.renderPath(d,o),this.addMarker("start",e(c.marker,c.startMarker),d),this.addMarker("end",e(c.marker,c.endMarker),d)},t.prototype.destroy=function(){this.graphics&&(a(this.graphics,function(t){t.destroy()}),delete this.graphics)},t}()}),i(n,"Series/PathUtilities.js",[],function(){function t(t,n){for(var i=[],r=0;r<t.length;r++){var e=t[r][1],a=t[r][2];if("number"==typeof e&&"number"==typeof a){if(0===r)i.push(["M",e,a]);else if(r===t.length-1)i.push(["L",e,a]);else if(n){var o=t[r-1],s=t[r+1];if(o&&s){var h=o[1],c=o[2],x=s[1],d=s[2];if("number"==typeof h&&"number"==typeof x&&"number"==typeof c&&"number"==typeof d&&h!==x&&c!==d){var M=h<x?1:-1,l=c<d?1:-1;i.push(["L",e-M*Math.min(Math.abs(e-h),n),a-l*Math.min(Math.abs(a-c),n)],["C",e,a,e,a,e+M*Math.min(Math.abs(e-x),n),a+l*Math.min(Math.abs(a-d),n)])}}}else i.push(["L",e,a])}}return i}return{applyRadius:t,getLinkPath:{default:function(n){var i=n.x1,r=n.y1,e=n.x2,a=n.y2,o=n.width,s=void 0===o?0:o,h=n.inverted,c=void 0!==h&&h,x=n.radius,d=n.parentVisible,M=[["M",i,r],["L",i,r],["C",i,r,i,a,i,a],["L",i,a],["C",i,r,i,a,i,a],["L",i,a]];return d?t([["M",i,r],["L",i+s*(c?-.5:.5),r],["L",i+s*(c?-.5:.5),a],["L",e,a]],x):M},straight:function(t){var n=t.x1,i=t.y1,r=t.x2,e=t.y2,a=t.width,o=t.inverted;return t.parentVisible?[["M",n,i],["L",n+(void 0===a?0:a)*(void 0!==o&&o?-1:1),e],["L",r,e]]:[["M",n,i],["L",n,e],["L",n,e]]},curved:function(t){var n=t.x1,i=t.y1,r=t.x2,e=t.y2,a=t.offset,o=void 0===a?0:a,s=t.width,h=void 0===s?0:s,c=t.inverted,x=void 0!==c&&c;return t.parentVisible?[["M",n,i],["C",n+o,i,n-o+h*(x?-1:1),e,n+h*(x?-1:1),e],["L",r,e]]:[["M",n,i],["C",n,i,n,e,n,e],["L",r,e]]}}}}),i(n,"Gantt/PathfinderAlgorithms.js",[n["Series/PathUtilities.js"],n["Core/Utilities.js"]],function(t,n){var i=n.pick,r=Math.min,e=Math.max,a=Math.abs;function o(t,n,i){for(var r,e,a=n-1e-7,o=i||0,s=t.length-1;o<=s;)if((e=a-t[r=s+o>>1].xMin)>0)o=r+1;else{if(!(e<0))return r;s=r-1}return o>0?o-1:0}function s(t,n){for(var i,r=o(t,n.x+1)+1;r--;)if(t[r].xMax>=n.x&&(i=t[r],n.x<=i.xMax&&n.x>=i.xMin&&n.y<=i.yMax&&n.y>=i.yMin))return r;return -1}function h(t){var n=[];if(t.length){n.push(["M",t[0].start.x,t[0].start.y]);for(var i=0;i<t.length;++i)n.push(["L",t[i].end.x,t[i].end.y])}return n}function c(t,n){t.yMin=e(t.yMin,n.yMin),t.yMax=r(t.yMax,n.yMax),t.xMin=e(t.xMin,n.xMin),t.xMax=r(t.xMax,n.xMax)}var x=function(n,r,e){var o,c,x,d,M,l=[],p=e.chartObstacles,f=s(p,n),y=s(p,r),u=i(e.startDirectionX,a(r.x-n.x)>a(r.y-n.y))?"x":"y";function g(t,n,i,r,e){var a={x:t.x,y:t.y};return a[n]=i[r||n]+(e||0),a}function v(t,n,i){var r=a(n[i]-t[i+"Min"])>a(n[i]-t[i+"Max"]);return g(n,i,t,i+(r?"Max":"Min"),r?1:-1)}y>-1?(o={start:x=v(p[y],r,u),end:r},M=x):M=r,f>-1&&(x=v(c=p[f],n,u),l.push({start:n,end:x}),x[u]>=n[u]==x[u]>=M[u]&&(d=n[u="y"===u?"x":"y"]<r[u],l.push({start:x,end:g(x,u,c,u+(d?"Max":"Min"),d?1:-1)}),u="y"===u?"x":"y"));var m=l.length?l[l.length-1].end:n;x=g(m,u,M),l.push({start:m,end:x});var b=g(x,u="y"===u?"x":"y",M);return l.push({start:x,end:b}),l.push(o),{path:t.applyRadius(h(l),e.radius),obstacles:l}};function d(t,n,x){var d,M,l,p,f,y,u,g=i(x.startDirectionX,a(n.x-t.x)>a(n.y-t.y)),v=g?"x":"y",m=[],b=x.obstacleMetrics,P=r(t.x,n.x)-b.maxWidth-10,C=e(t.x,n.x)+b.maxWidth+10,w=r(t.y,n.y)-b.maxHeight-10,k=e(t.y,n.y)+b.maxHeight+10,O=!1,L=x.chartObstacles,j=o(L,C),A=o(L,P);function E(t,n,i){var e,a,s,h,c=t.x<n.x?1:-1;t.x<n.x?(e=t,a=n):(e=n,a=t),t.y<n.y?(h=t,s=n):(h=n,s=t);for(var x=c<0?r(o(L,a.x),L.length-1):0;L[x]&&(c>0&&L[x].xMin<=a.x||c<0&&L[x].xMax>=e.x);){if(L[x].xMin<=a.x&&L[x].xMax>=e.x&&L[x].yMin<=s.y&&L[x].yMax>=h.y){if(i)return{y:t.y,x:t.x<n.x?L[x].xMin-1:L[x].xMax+1,obstacle:L[x]};return{x:t.x,y:t.y<n.y?L[x].yMin-1:L[x].yMax+1,obstacle:L[x]}}x+=c}return n}function G(t,n,i,r,e){var o=e.soft,s=e.hard,h=r?"x":"y",c={x:n.x,y:n.y},x={x:n.x,y:n.y},d=t[h+"Max"]>=o[h+"Max"],M=t[h+"Min"]<=o[h+"Min"],l=t[h+"Max"]>=s[h+"Max"],p=t[h+"Min"]<=s[h+"Min"],f=a(t[h+"Min"]-n[h]),y=a(t[h+"Max"]-n[h]),u=10>a(f-y)?n[h]<i[h]:y<f;x[h]=t[h+"Min"],c[h]=t[h+"Max"];var g=E(n,x,r)[h]!==x[h],v=E(n,c,r)[h]!==c[h];return u=g?!v||u:!v&&u,u=M?!d||u:!d&&u,u=p?!l||u:!l&&u}for((j=s(L=L.slice(A,j+1),n))>-1&&(d=L[j],M=n,l=r(d.xMax-M.x,M.x-d.xMin)<r(d.yMax-M.y,M.y-d.yMin),p=G(d,M,t,l,{soft:x.hardBounds,hard:x.hardBounds}),m.push({end:n,start:u=l?{y:M.y,x:d[p?"xMax":"xMin"]+(p?1:-1)}:{x:M.x,y:d[p?"yMax":"yMin"]+(p?1:-1)}}),n=u);(j=s(L,n))>-1;)y=n[v]-t[v]<0,(u={x:n.x,y:n.y})[v]=L[j][y?v+"Max":v+"Min"]+(y?1:-1),m.push({end:n,start:u}),n=u;return{path:h(f=(f=function t(n,i,a){if(n.x===i.x&&n.y===i.y)return[];var o,h,d,M,l,p,f,y=a?"x":"y",u=x.obstacleOptions.margin,g={soft:{xMin:P,xMax:C,yMin:w,yMax:k},hard:x.hardBounds};return(l=s(L,n))>-1?(M=G(l=L[l],n,i,a,g),c(l,x.hardBounds),f=a?{y:n.y,x:l[M?"xMax":"xMin"]+(M?1:-1)}:{x:n.x,y:l[M?"yMax":"yMin"]+(M?1:-1)},(p=s(L,f))>-1&&(c(p=L[p],x.hardBounds),f[y]=M?e(l[y+"Max"]-u+1,(p[y+"Min"]+l[y+"Max"])/2):r(l[y+"Min"]+u-1,(p[y+"Max"]+l[y+"Min"])/2),n.x===f.x&&n.y===f.y?(O&&(f[y]=M?e(l[y+"Max"],p[y+"Max"])+1:r(l[y+"Min"],p[y+"Min"])-1),O=!O):O=!1),h=[{start:n,end:f}]):(o=E(n,{x:a?i.x:n.x,y:a?n.y:i.y},a),h=[{start:n,end:{x:o.x,y:o.y}}],o[a?"x":"y"]!==i[a?"x":"y"]&&(M=G(o.obstacle,o,i,!a,g),c(o.obstacle,x.hardBounds),d={x:a?o.x:o.obstacle[M?"xMax":"xMin"]+(M?1:-1),y:a?o.obstacle[M?"yMax":"yMin"]+(M?1:-1):o.y},a=!a,h=h.concat(t({x:o.x,y:o.y},d,a)))),h=h.concat(t(h[h.length-1].end,i,!a))}(t,n,g)).concat(m.reverse())),obstacles:f}}return x.requiresObstacles=!0,d.requiresObstacles=!0,{fastAvoid:d,straight:function(t,n){return{path:[["M",t.x,t.y],["L",n.x,n.y]],obstacles:[{start:t,end:n}]}},simpleConnect:x}}),i(n,"Gantt/ConnectorsDefaults.js",[],function(){return{connectors:{type:"straight",radius:0,lineWidth:1,marker:{enabled:!1,align:"center",verticalAlign:"middle",inside:!1,lineWidth:1},startMarker:{symbol:"diamond"},endMarker:{symbol:"arrow-filled"}}}}),i(n,"Gantt/PathfinderComposition.js",[n["Gantt/ConnectorsDefaults.js"],n["Core/Defaults.js"],n["Core/Utilities.js"]],function(t,n,i){var r,e=n.setOptions,a=i.defined,o=i.error,s=i.merge;function h(t){var n=t.shapeArgs;if(n)return{xMin:n.x||0,xMax:(n.x||0)+(n.width||0),yMin:n.y||0,yMax:(n.y||0)+(n.height||0)};var i=t.graphic&&t.graphic.getBBox();return i?{xMin:t.plotX-i.width/2,xMax:t.plotX+i.width/2,yMin:t.plotY-i.height/2,yMax:t.plotY+i.height/2}:null}return function(n){function i(t){var n,i,r=h(this);switch(t.align){case"right":n="xMax";break;case"left":n="xMin"}switch(t.verticalAlign){case"top":i="yMin";break;case"bottom":i="yMax"}return{x:n?r[n]:(r.xMin+r.xMax)/2,y:i?r[i]:(r.yMin+r.yMax)/2}}function r(t,n){var i;return!a(n)&&(i=h(this))&&(n={x:(i.xMin+i.xMax)/2,y:(i.yMin+i.yMax)/2}),Math.atan2(n.y-t.y,t.x-n.x)}function c(t,n,i){for(var r=2*Math.PI,e=h(this),a=e.xMax-e.xMin,o=e.yMax-e.yMin,s=Math.atan2(o,a),c=a/2,x=o/2,d=e.xMin+c,M=e.yMin+x,l={x:d,y:M},p=t,f=1,y=!1,u=1,g=1;p<-Math.PI;)p+=r;for(;p>Math.PI;)p-=r;return f=Math.tan(p),p>-s&&p<=s?(g=-1,y=!0):p>s&&p<=Math.PI-s?g=-1:p>Math.PI-s||p<=-(Math.PI-s)?(u=-1,y=!0):u=-1,y?(l.x+=u*c,l.y+=g*c*f):(l.x+=o/(2*f)*u,l.y+=g*x),i.x!==d&&(l.x=i.x),i.y!==M&&(l.y=i.y),{x:l.x+n*Math.cos(p),y:l.y-n*Math.sin(p)}}n.compose=function(n,a,h){var x=h.prototype;x.getPathfinderAnchorPoint||(n.prototype.callbacks.push(function(t){!1!==t.options.connectors.enabled&&((t.options.pathfinder||t.series.reduce(function(t,n){return n.options&&s(!0,n.options.connectors=n.options.connectors||{},n.options.pathfinder),t||n.options&&n.options.pathfinder},!1))&&(s(!0,t.options.connectors=t.options.connectors||{},t.options.pathfinder),o('WARNING: Pathfinder options have been renamed. Use "chart.connectors" or "series.connectors" instead.')),this.pathfinder=new a(this),this.pathfinder.update(!0))}),x.getMarkerVector=c,x.getPathfinderAnchorPoint=i,x.getRadiansToVector=r,e(t))}}(r||(r={})),r}),i(n,"Gantt/Pathfinder.js",[n["Gantt/Connection.js"],n["Gantt/PathfinderAlgorithms.js"],n["Gantt/PathfinderComposition.js"],n["Core/Series/Point.js"],n["Core/Utilities.js"]],function(t,n,i,r,e){var a=e.addEvent,o=e.defined,s=e.pick,h=e.splat,c=Math.max,x=Math.min,d=function(){function n(t){this.init(t)}return n.compose=function(t,r){i.compose(t,n,r)},n.prototype.init=function(t){this.chart=t,this.connections=[],a(t,"redraw",function(){this.pathfinder.update()})},n.prototype.update=function(n){var i=this.chart,e=this,a=e.connections;e.connections=[],i.series.forEach(function(n){n.visible&&!n.options.isInternal&&n.points.forEach(function(n){var a,o,s=n.options;s&&s.dependency&&(s.connect=s.dependency);var c=(null===(a=n.options)||void 0===a?void 0:a.connect)&&h(n.options.connect);n.visible&&!1!==n.isInside&&c&&c.forEach(function(a){(o=i.get("string"==typeof a?a:a.to))instanceof r&&o.series.visible&&o.visible&&!1!==o.isInside&&e.connections.push(new t(n,o,"string"==typeof a?{}:a))})})});for(var o=0,s=void 0,c=void 0,x=a.length,d=e.connections.length;o<x;++o){c=!1;var M=a[o];for(s=0;s<d;++s){var l=e.connections[s];if((M.options&&M.options.type)===(l.options&&l.options.type)&&M.fromPoint===l.fromPoint&&M.toPoint===l.toPoint){l.graphics=M.graphics,c=!0;break}}c||M.destroy()}delete this.chartObstacles,delete this.lineObstacles,e.renderConnections(n)},n.prototype.renderConnections=function(t){t?this.chart.series.forEach(function(t){var n=function(){var n=t.chart.pathfinder;(n&&n.connections||[]).forEach(function(n){n.fromPoint&&n.fromPoint.series===t&&n.render()}),t.pathfinderRemoveRenderEvent&&(t.pathfinderRemoveRenderEvent(),delete t.pathfinderRemoveRenderEvent)};!1===t.options.animation?n():t.pathfinderRemoveRenderEvent=a(t,"afterAnimate",n)}):this.connections.forEach(function(t){t.render()})},n.prototype.getChartObstacles=function(t){for(var n,i=this.chart.series,r=s(t.algorithmMargin,0),e=[],a=0,h=i.length;a<h;++a)if(i[a].visible&&!i[a].options.isInternal)for(var d=0,M=i[a].points.length,l=void 0,p=void 0;d<M;++d)(p=i[a].points[d]).visible&&(l=function(t){var n=t.shapeArgs;if(n)return{xMin:n.x||0,xMax:(n.x||0)+(n.width||0),yMin:n.y||0,yMax:(n.y||0)+(n.height||0)};var i=t.graphic&&t.graphic.getBBox();return i?{xMin:t.plotX-i.width/2,xMax:t.plotX+i.width/2,yMin:t.plotY-i.height/2,yMax:t.plotY+i.height/2}:null}(p))&&e.push({xMin:l.xMin-r,xMax:l.xMax+r,yMin:l.yMin-r,yMax:l.yMax+r});return e=e.sort(function(t,n){return t.xMin-n.xMin}),o(t.algorithmMargin)||(n=t.algorithmMargin=function(t){for(var n,i=t.length,r=[],e=0;e<i;++e)for(var a=e+1;a<i;++a)(n=function t(n,i,r){var e=s(r,10),a=n.yMax+e>i.yMin-e&&n.yMin-e<i.yMax+e,o=n.xMax+e>i.xMin-e&&n.xMin-e<i.xMax+e,h=a?n.xMin>i.xMax?n.xMin-i.xMax:i.xMin-n.xMax:1/0,c=o?n.yMin>i.yMax?n.yMin-i.yMax:i.yMin-n.yMax:1/0;return o&&a?e?t(n,i,Math.floor(e/2)):1/0:x(h,c)}(t[e],t[a]))<80&&r.push(n);return r.push(80),c(Math.floor(r.sort(function(t,n){return t-n})[Math.floor(r.length/10)]/2-1),1)}(e),e.forEach(function(t){t.xMin-=n,t.xMax+=n,t.yMin-=n,t.yMax+=n})),e},n.prototype.getObstacleMetrics=function(t){for(var n,i,r=0,e=0,a=t.length;a--;)n=t[a].xMax-t[a].xMin,i=t[a].yMax-t[a].yMin,r<n&&(r=n),e<i&&(e=i);return{maxHeight:e,maxWidth:r}},n.prototype.getAlgorithmStartDirection=function(t){var n="left"!==t.align&&"right"!==t.align,i="top"!==t.verticalAlign&&"bottom"!==t.verticalAlign;return n?!!i&&void 0:!!i||void 0},n}();return d.prototype.algorithms=n,d}),i(n,"Extensions/ArrowSymbols.js",[],function(){function t(t,n,i,r){return[["M",t,n+r/2],["L",t+i,n],["L",t,n+r/2],["L",t+i,n+r]]}function n(n,i,r,e){return t(n,i,r/2,e)}function i(t,n,i,r){return[["M",t+i,n],["L",t,n+r/2],["L",t+i,n+r],["Z"]]}function r(t,n,r,e){return i(t,n,r/2,e)}return{compose:function(e){var a=e.prototype.symbols;a.arrow=t,a["arrow-filled"]=i,a["arrow-filled-half"]=r,a["arrow-half"]=n,a["triangle-left"]=i,a["triangle-left-half"]=r}}}),i(n,"masters/modules/pathfinder.src.js",[n["Core/Globals.js"],n["Gantt/Pathfinder.js"],n["Extensions/ArrowSymbols.js"]],function(t,n,i){return t.Pathfinder=t.Pathfinder||n,i.compose(t.SVGRenderer),t.Pathfinder.compose(t.Chart,t.Point),t})});