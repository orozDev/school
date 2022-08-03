let box = document.getElementsByClassName('brand-image');
let box2 = document.getElementsByClassName('login-logo');
let footer = document.getElementsByClassName('main-footer')

try{
    box[0].setAttribute('src', '/static/img/oroz.gif');
    box[0].removeAttribute("style");
}
catch(e){}

try{
    let img = box2[0].children[0].children[0];
    img.setAttribute('width', '80%')
}
catch(e){}

try{
    footer[0].children[0].innerHTML = '<b>+996 776 78 04 72</b>';
}
catch(e){}

try{
   let user_logo = document.getElementsByClassName('image')[0];
   user_logo.children[0]
}
catch(e){}

function include(url, integrity=null, crossorigin=null) {
    let script = document.createElement('script');
    script.src = url;
    if(integrity != null) script.setAttribute('integrity', integrity);
    if(crossorigin != null) script.setAttribute('crossorigin', crossorigin);
    document.getElementsByTagName('head')[0].appendChild(script);   
}
