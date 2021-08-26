var updateBtns = document.getElementsByClassName('update-cart')

for(var i = 0; i < updateBtns.length; i++){
  updateBtns[i].addEventListener('click', function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    console.log('productID:', productId, 'action:', action)
    console.log('USER', user)
    if (user == 'AnonymousUser') {
      addCookieItem(productId, action)
    }else{
      updateUserOrder(productId,action)
    }
  })
}

function addCookieItem(productId, action){
  console.log('User is not authenticated')
  if(action == 'add'){
    var night = $("#nights").val()
    var q = parseInt(night);
    if(cart[productId] == undefined){
      cart[productId] = {'quantity':q}
    }else{
      cart[productId]['quantity'] = q
    }
  }

  if(action == 'remove'){
    cart[productId]['quantity'] = 0
    if(cart[productId]['quantity'] <= 0) {
      console.log('Item should be deleted')
      delete cart[productId];
    }
  }
  console.log('Cart:',cart)
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
  location.reload()
}

function updateUserOrder(productId, action){
  console.log('User is logged in, sending data..')
  var url = '/update_item/'
  //console.log('URL:',url)
  fetch(url, {
    method:'POST',
    headers:{
      'Content-Type':'application/json',
      'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({'productId':productId, 'action':action})
  })

  .then((response)=>{
    return response.json()
  })

  .then((data)=>{
    console.log('data:', data)
    location.reload()
  })

}
