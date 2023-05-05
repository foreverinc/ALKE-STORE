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
        stars[j].classList.remove("text-warning");
      }
      stars[0].classList.add("text-warning");
    } else if (rated === "2") {
      for (var j = 0; j < stars.length; j++) {
        stars[j].classList.remove("text-warning");
      }
      stars[0].classList.add("text-warning");
      stars[1].classList.add("text-warning");
    } else if (rated === "3") {
      for (var j = 0; j < stars.length; j++) {
        stars[j].classList.remove("text-warning");
      }
      stars[0].classList.add("text-warning");
      stars[1].classList.add("text-warning");
      stars[2].classList.add("text-warning");
    } else if (rated === "4") {
      for (var j = 0; j < stars.length; j++) {
        stars[j].classList.remove("text-warning");
      }
      stars[0].classList.add("text-warning");
      stars[1].classList.add("text-warning");
      stars[2].classList.add("text-warning");
      stars[3].classList.add("text-warning");
    } else if (rated === "5") {
      for (var j = 0; j < stars.length; j++) {
        stars[j].classList.remove("text-warning");
      }
      stars[0].classList.add("text-warning");
      stars[1].classList.add("text-warning");
      stars[2].classList.add("text-warning");
      stars[3].classList.add("text-warning");
      stars[4].classList.add("text-warning");
    }
    document.getElementById('ratings').value = rating
  });
}



let QuantityBtns = document.getElementsByClassName("update-quantity");
let quantity = document.getElementById("quantity");
for (var i = 0; i < QuantityBtns.length; i++) {
  QuantityBtns[i].addEventListener("click", function () {
    var action = this.dataset.action;
    console.log(action);
    if (action === "add") {
      quantity.value = parseInt(quantity.value) + 1;
    } else if (action === "remove") {
      if (quantity.value > 1) {
        // check if value is already 1 or above
        quantity.value = parseInt(quantity.value) - 1;
      }
    }
  });
}
