// Ayan Chakrabarti <ayan.chakrabarti@gmail.com>

showIndiv = function() {
    group = parseInt(document.querySelector('#group').value);
    exp = parseInt(document.querySelector('#exp').value);
    indiv = parseInt(document.querySelector('#indiv').value);

    imgs = data[group][3][exp][1][indiv];
    for(i = 0; i < imgs.length; i++) {
        imgi = imgs[i];
        if(Array.isArray(imgi)) {
            texti = imgi[1]; imgi = imgi[0];
        } else
            texti = "";
        document.querySelector("#lnk"+i).setAttribute("href", imgi);
        document.querySelector("#img"+i).setAttribute("src", imgi);
        document.querySelector("#lbl"+i).innerHTML = texti;
    }
    history.replaceState(undefined, undefined, "#"+group+"#"+exp+"#"+indiv);
}

iswitch = function(delta) {
    group = parseInt(document.querySelector('#group').value);
    exp = parseInt(document.querySelector('#exp').value);
    indiv = parseInt(document.querySelector('#indiv').value);

    indiv = indiv + delta;
    if(indiv < 0) indiv = 0;
    if(indiv >= data[group][2].length) indiv = data[group][2].length-1;
    document.querySelector('#indiv').selectedIndex = indiv;
    showIndiv();
}

eswitch = function(delta) {
    group = parseInt(document.querySelector('#group').value);
    exp = parseInt(document.querySelector('#exp').value);
    indiv = parseInt(document.querySelector('#indiv').value);

    exp = exp  + delta;
    if(exp < 0) exp = 0;
    if(exp >= data[group][3].length) exp = data[group][3].length-1;
    document.querySelector('#exp').selectedIndex = exp;
    showIndiv();
}

showGroup = function(val, exp, indiv) {
    html = ''; sublist = data[val][3];
    for(i = 0; i < sublist.length; i++) {
        if(i == exp)
            html = html + '<option selected="selected" value='+i+'>'+sublist[i][0]+'</option>';
        else
            html = html + '<option value='+i+'>'+sublist[i][0]+'</option>';
    }
    document.querySelector('#exp').innerHTML = html;

    html = ''; inlist = data[val][2];
    for(i = 0; i < inlist.length; i++) {
        if(i == indiv)
            html = html + '<option selected="selected" value='+i+'>'+inlist[i]+'</option>';
        else
            html = html + '<option value='+i+'>'+inlist[i]+'</option>';
    }
    document.querySelector('#indiv').innerHTML = html;

    html = ''; columns = data[val][1];
    for(i = 0; i < columns.length; i++) {
        html = html + '<div class="column"><a id="lnk'+i+'" target=_blank><img id="img'+i+'"></a>';
        html = html + '<br/><span style="color: #ebe;" id="lbl'+i+'"></span><br/>'+columns[i]+'</div>';
    }
    document.querySelector('#gallery').innerHTML = html;

    showIndiv();
}

groupChg = function(val) {
    val = parseInt(val);
    showGroup(parseInt(val), 0, 0);
}

onKey = function(e) {
    if(e.keyCode == 106) {iswitch(1); return false;}
    if(e.keyCode == 107) {iswitch(-1); return false;}

    if(e.keyCode == 104) {eswitch(-1); return false;}
    if(e.keyCode == 108) {eswitch(1); return false;}
}

window.onload = function() {
    document.body.innerHTML = `
        <div class="head">
            <div>
                <table><tr style="vertical-align: center;">
                    <td id="title">StaticBoard</td>
                    <td><select style="width: 250px;" id='group' onclick='javascript:groupChg(this.value);' onchange='javascript:groupChg(this.value);'></select></td>
                </tr></table>
            </div>
        </div>
        <div class="graph">
            <div id="selector">
                <button onclick="javascript:eswitch(-1);">Prev (h)</button>
                <select style="width: 200px;" id='exp' onclick='javascript:showIndiv();' onchange='javascript:showIndiv();'></select>
                <button onclick="javascript:eswitch(-1);">Next (l)</button>

                &nbsp;&nbsp;&nbsp;

                List: <button onclick="javascript:iswitch(-1);">Prev (k)</button>
                <select style="width: 200px;" id='indiv' onclick='javascript:showIndiv();' onchange='javascript:showIndiv();'></select>
                <button onclick="javascript:iswitch(1);">Next (j)</button>
            </div>
            <div id="gallery"></div>
        </div>
`;

    // Setup list of groups
    hash = window.location.hash.split('#');
    if(hash.length < 4) {
        selgroup = 0; selexp = 0; selind = 0;
    } else {
        selgroup = parseInt(hash[1]);
        selexp = parseInt(hash[2]);
        selind = parseInt(hash[3]);
    }

    html = '';
    for(i = 0; i < data.length; i++) {
        if(i == selgroup)
            html = html + '<option selected="selected" value='+i+'>'+data[i][0]+'</option>';
        else
            html = html + '<option value='+i+'>'+data[i][0]+'</option>';
    }
    document.querySelector('#group').innerHTML = html;
    showGroup(selgroup, selexp, selind);

    document.onkeypress = onKey;
};
