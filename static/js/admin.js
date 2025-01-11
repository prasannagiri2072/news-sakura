// static/js/admin.js  
  
document.addEventListener('DOMContentLoaded', function() {  
    // Initialize Bootstrap Tabs  
    var triggerTabList = [].slice.call(document.querySelectorAll('#adminTab button'))  
    triggerTabList.forEach(function (triggerEl) {  
        var tabTrigger = new bootstrap.Tab(triggerEl)  
  
        triggerEl.addEventListener('click', function (event) {  
            event.preventDefault()  
            tabTrigger.show()  
        })  
    });  
});  