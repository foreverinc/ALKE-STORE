let updateBtns = document.getElementsByClassName('update-cart')
for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        updateUserOrder(productId,action)
    })
}

function updateUserOrder(productId, action) {
  var url = "/update/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId, action: action }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      document.getElementById("itemnum").innerHTML = data;
      alert('Added to cart')
       
        
    });
}

let stars = document.getElementsByClassName("rater");
let rating = 0;
for (var i = 0; i < stars.length; i++) {
  stars[i].addEventListener("click", function () {
    var rated = this.dataset.rate;
    rating = parseInt(rated);
    if (rated === "1") {
      for (var j = 0; j < stars.length; j++) {
        stars[j].classList.remove("text-primary");
      }
      stars[0].classList.add("text-primary");
    } else if (rated === "2") {
      for (var j = 0; j < stars.length; j++) {
        stars[j].classList.remove("text-primary");
      }
      stars[0].classList.add("text-primary");
      stars[1].classList.add("text-primary");
    } else if (rated === "3") {
      for (var j = 0; j < stars.length; j++) {
        stars[j].classList.remove("text-primary");
      }
      stars[0].classList.add("text-primary");
      stars[1].classList.add("text-primary");
      stars[2].classList.add("text-primary");
    } else if (rated === "4") {
      for (var j = 0; j < stars.length; j++) {
        stars[j].classList.remove("text-primary");
      }
      stars[0].classList.add("text-primary");
      stars[1].classList.add("text-primary");
      stars[2].classList.add("text-primary");
      stars[3].classList.add("text-primary");
    } else if (rated === "5") {
      for (var j = 0; j < stars.length; j++) {
        stars[j].classList.remove("text-primary");
      }
      stars[0].classList.add("text-primary");
      stars[1].classList.add("text-primary");
      stars[2].classList.add("text-primary");
      stars[3].classList.add("text-primary");
      stars[4].classList.add("text-primary");
    }
    document.getElementById('ratings').value = rating
  });
}




let wishesBtn = document.getElementsByClassName("update-wish");
for (var i = 0; i < wishesBtn.length; i++) {
  wishesBtn[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    updateUserWishlist(productId);
  });
}

function updateUserWishlist(productId) {
  var url = "/wishlist/";
  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ productId: productId}),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      document.getElementById("wishnum").innerHTML = data;
      alert("Added to Wishlist");
    });
}
