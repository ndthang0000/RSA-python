document.addEventListener("DOMContentLoaded",(e)=>{
    
    //log out
    let btnLogOut=document.querySelector('#log-out')
    btnLogOut.addEventListener('click', (e)=>{
        localStorage.setItem('isLogin', JSON.stringify(false))
        window.location.href=window.location.pathname.replace('index','login')
    })

    
    // toggle image avatar
    const imageBtn=document.querySelector('.image-area')
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
    console.log(menuEl)
    menuEl.forEach(item=>{
        console.log(item.href)
        if(item.href===location.href){
            item.classList.add('active')
        }
    })
    

    // side bar menu
    const headerEl=document.querySelector('.header-logo')
    const sideBarEl=document.querySelector('.side-bar-menu')
    headerEl.addEventListener('click',(e)=>{
        sideBarEl.classList.toggle('hidden-side-bar')
    })
})