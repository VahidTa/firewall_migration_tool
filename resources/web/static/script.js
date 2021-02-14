function ChangeDropdowns(value){
    if(value=="netconf" || value=="rest"){
        document.getElementById('file').style.display='none';
        for (i = 0; i < 4; i++){
            document.getElementsByClassName('remote')[i].style.display='block';
        }
        document.getElementById('host').setAttribute('required', true);
        document.getElementById('username').setAttribute('required', true);
        document.getElementById('password').setAttribute('required', true);
        document.getElementById('port').setAttribute('required', true);
        if(value=="rest"){
            document.getElementById('protocol').setAttribute('required', true);
            document.getElementsByClassName('protocol')[0].style.display='block';
        }
        if(value=="netconf"){
            document.getElementById('protocol').removeAttribute('required');
            document.getElementsByClassName('protocol')[0].style.display='none';
        }
    }else if(value=="file"){
        document.getElementById('file').style.display='block';
        for (i = 0; i < 4; i++) {
            document.getElementsByClassName('remote')[i].style.display='none';
        }
        document.getElementsByClassName('protocol')[0].style.display='none';
        document.getElementById('host').removeAttribute('required');
        document.getElementById('username').removeAttribute('required');
        document.getElementById('password').removeAttribute('required');
        document.getElementById('protocol').removeAttribute('required');
        document.getElementById('port').removeAttribute('required');
        document.getElementById('protocol').removeAttribute('required');
    }
}

function configOptions(value) {
    if(value=='config'){
        document.getElementById('config-box').style.display='block';
    }
    else if(value=='policy'){
        document.getElementById('config-box').style.display='none';
    }
}


function updateSelect(changedSelect, selectId) {
    var otherSelect = document.getElementById(selectId);
    for (var i = 0; i < otherSelect.options.length; ++i) {
      otherSelect.options[i].disabled = false;
    }
    if (changedSelect.selectedIndex == 0) {
      return;
    }
    otherSelect.options[changedSelect.selectedIndex].disabled = true;
  }


