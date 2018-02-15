var state=0;
var visT = [];
var visE = [];

var hash1 = '';

makeHash = function() {
    vhash='';
    ehash='';
    for(i = 0; i < exps.length;i++) {
	if(visT[exps[i]] == undefined || visT[exps[i]] == true)
	    vhash = vhash + '1';
	else
	    vhash=vhash+'0';
    }
    for(i = 0; i < tags.length;i++) {
	if(visE[tags[i]] == undefined || visE[tags[i]] == true)
	    ehash = ehash + '1';
	else
	    ehash=ehash+'0';
    }
    history.replaceState(undefined, undefined, "#"+hash1+'#'+vhash+'#'+ehash);
}

loadHash = function(hs) {
    if(hs.length >= 3) vhash = hs[2]; else vhash = '';
    if(hs.length >= 4) ehash = hs[3]; else ehash = '';

    for(i = 0; i < exps.length && i < vhash.length;i++)
	if(vhash.substring(i,i+1) == '0')
	    visT[exps[i]] = 'legendonly';

    for(i = 0; i < tags.length && i < ehash.length;i++)
	if(ehash.substring(i,i+1) == '0')
	    visE[tags[i]] = 'legendonly';
}

noteVis = function() {
    od = document.getElementById('graph').data;
    if(state == 1) {
	for(i=0;i<od.length;i++)
	    visT[od[i].name] = od[i].visible;
    }
   if(state == 2) {
	for(i=0;i<od.length;i++)
	    visE[od[i].name] = od[i].visible;
   }    
}

svgE = {name: 'toSVG',icon: Plotly.Icons.camera,click: function(gd) {
      Plotly.downloadImage(gd, {format: 'svg'})
}};

showTag = function (tag) {
    d = []; noteVis();
    for(i = 0; i < exps.length;i++) {
        if(!data[tag+'@'+exps[i]]) continue;
        el = {};
	el.name = exps[i]; el.mode = "lines"; el.line = {width: 2.0};
	el.x = data[tag+'@'+exps[i]].x;
	el.y = data[tag+'@'+exps[i]].y;
	if(visT[exps[i]] != undefined) el.visible = visT[exps[i]];
	el.hoverlabel = {namelength: -1}; d.push(el);
    }
    for(i = 0; i < tags.length;i++)
        if(tags[i] == tag)
            hash1 = "v"+i;
    document.querySelector('#graph').innerHTML = '';
    document.querySelector('#desc').innerHTML = tag + ' @ *';
    Plotly.newPlot('graph',d,{hovermode: 'x', margin: {l: 50, r: 100, b: 50, t: 50},xaxis: {nticks: 20}, yaxis: {nticks: 25}}, {showTips: false, displayModeBar: true, modeBarButtonsToRemove: ['sendDataToCloud','hoverClosestCartesian','hoverCompareCartesian','toggleSpikelines','toImage'],modeBarButtonsToAdd:[svgE]});
    state = 1;
    makeHash();
    document.querySelector('#graph').on('plotly_afterplot', function() {noteVis();makeHash();});
};

showExp = function (exp) {
    d = []; noteVis();
    for(i = 0; i < tags.length;i++) {
        if(!data[tags[i]+'@'+exp]) continue;
        el = {};
	el.name = tags[i]; el.mode = "lines"; el.line = {width: 2.0};
	el.x = data[tags[i]+'@'+exp].x;
	el.y = data[tags[i]+'@'+exp].y;
	if(visE[tags[i]] != undefined) el.visible = visE[tags[i]];
	el.hoverlabel = {namelength: -1}; d.push(el);
    }
    for(i = 0; i < exps.length;i++)
        if(exps[i] == exp)
            hash1 = 'e'+i;
    document.querySelector('#graph').innerHTML = '';
    document.querySelector('#desc').innerHTML = '* @ ' + exp;
    Plotly.newPlot('graph',d,{hovermode: 'x', margin: {l: 50, r: 100, b: 50, t: 50},xaxis: {nticks: 20}, yaxis: {nticks: 25}}, {showTips: false, displayModeBar: true, modeBarButtonsToRemove: ['sendDataToCloud','hoverClosestCartesian','hoverCompareCartesian','toggleSpikelines','toImage'],modeBarButtonsToAdd:[svgE]});
    state=2;
    makeHash();
    document.querySelector('#graph').on('plotly_afterplot', function() {noteVis();makeHash();});
};


onKey = function(e) {
    if(e.keyCode == 118) {el = document.querySelector('#byvar'); el.focus(); showTag(el.value); return false;}
    if(e.keyCode == 101) {el = document.querySelector('#byexp'); el.focus(); showExp(el.value); return false;}
}

window.onload = function (e) {
    document.body.innerHTML=`
<div class='head'><div class='container'><table><tr style='vertical-align: center;'>
<td id='title'>StaticBoard</td><td>
&nbsp;&nbsp;&nbsp;&nbsp;By Var: <select style="width: 250px;" id='byvar' onclick='javascript:showTag(this.value);' onchange='javascript:showTag(this.value);'> </select> 
&nbsp;&nbsp;&nbsp;&nbsp;By Exp: <select style="width: 250px;" id='byexp' onclick='javascript:showExp(this.value);' onchange='javascript:showExp(this.value);'> </select>
</td></tr></table></div></div><div class='container'>
<p>Showing: <span id="desc"></span></p>
<div id='graph' style='background: #fff; width: 1240px; height: 600px; margin: auto;'></div>
</div>
`;
    
    var html = '';
    
    hs=window.location.hash.split('#');
    loadHash(hs);
    if(hs.length < 2)
        {if(exps.length > 1) showTag(tags[0]); else showExp(exps[0]);}
    else {
	nm = parseInt(hs[1].substring(1,hs[1].length));
	if(isNaN(nm))
	   {if(exps.length > 1) showTag(tags[0]); else showExp(exps[0]);}
	else {
            if(hs[1].substring(0,1) == "e") showExp(exps[nm]);
	    else if(hs[1].substring(0,1) == "v") showTag(tags[nm]);
	    else if(exps.length > 1) showTag(tags[0]);
	    else showExp(exps[0]);
	}
    }
    for(i = 0; i < tags.length;i++) {
	if(hs[1] == "v"+i)
	    html = html+'<option selected="selected" value="'+tags[i]+'">'+tags[i]+'</option>';
	else
            html = html+'<option value="'+tags[i]+'">'+tags[i]+'</option>';
    }
    document.querySelector('#byvar').innerHTML=html;
    html = '';
    for(i = 0; i < exps.length;i++) {
	if(hs[1] == "e"+i)
            html = html+'<option selected="selected" value="'+exps[i]+'">'+exps[i]+'</option>';
	else
	    html = html+'<option value="'+exps[i]+'">'+exps[i]+'</option>';
    }
    document.querySelector('#byexp').innerHTML=html;

    
    document.onkeypress = onKey;
}
