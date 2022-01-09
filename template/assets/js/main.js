let token=localStorage.getItem('token')

function canvasArrToString(pix) {
    var s="";
    // Removes alpha to save space.
    for (var i=0; i<pix.length; i+=4) {
        s+=(String.fromCharCode(pix[i])
            + String.fromCharCode(pix[i+1])
            + String.fromCharCode(pix[i+2]));
    }
    return s;
}

function canvasStringToArr(s) {
    var arr=[];
    for (var i=0; i<s.length; i+=3) {
        for (var j=0; j<3; j++) {
        arr.push(s.substring(i+j,i+j+1).charCodeAt());
        }
        arr.push(255); // Hardcodes alpha to 255.
    }
    return arr;
}
document.addEventListener("DOMContentLoaded",(e)=>{
    
    //log out
    let btnLogOut=document.querySelector('#log-out')
    if(btnLogOut){
        btnLogOut.addEventListener('click', (e)=>{
            localStorage.setItem('isLogin', JSON.stringify(false))
            window.location.href=window.location.pathname.replace('index','login')
        })
    }
    

    
    // toggle image avatar
    const logoutEl=document.querySelector('.list-item')
    document.addEventListener('click',(e)=>{
        if(e.target.classList.value==='img-avatar'){
            logoutEl.classList.toggle('ds-none-block')
        }
        else{
            logoutEl.classList.add('ds-none-block')
        }
        
    })


    // active menu item
    const menuEl=document.querySelectorAll('.menu-list a')
    menuEl.forEach(item=>{
        if(item.href===location.href){
            item.classList.add('active')
        }
    })
    

    // side bar menu
    const headerEl=document.querySelector('.header-logo')
    const sideBarEl=document.querySelector('.side-bar-menu')
    if(headerEl){
        headerEl.addEventListener('click',(e)=>{
            sideBarEl.classList.toggle('hidden-side-bar')
        })
    }
    
})