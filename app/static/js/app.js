products = [
        {
            'id': 1001,
            'title': 'Soap',
            'price': 3.98,
            'desc': 'Very clean soapy soap, descriptive text'
        },
        {
            'id': 1002,
            'title': 'Grapes',
            'price': 4.56,
            'desc': 'A bundle of grapey grapes, yummy'
        },
        {
            'id': 1003,
            'title': 'Pickles',
            'price': 5.67,
            'desc': 'A jar of pickles is pickly'
        },
        {
            'id': 1004,
            'title': 'Juice',
            'price': 2.68,
            'desc': 'Yummy orange juice'
        }
    ]

/****************************
Start cart operation functions
*******************************/

  // create add item function to push to cart
function addItem(id) {
  // clear session storage
  // sessionStorage.clear();
  console.log(id);

  if (sessionStorage.getItem('cart')) {
    var cart = JSON.parse(sessionStorage.getItem('cart'));
  } else {
    var cart = [];
  }

  // check to see if a cartt key exists in session storage

// if it does, set a local cart variable to work with, using the parsed string

// if it does not exist, set up an empty array

// loop through global products variable and push to cart

  for (let i in products) {
    if (products[i].id == id) {
      cart.push(products[i]);
      break;
    }
  }

  // store the cart into the session storage
  sessionStorage.setItem('cart', JSON.stringify(cart));
}


// create a remove item function that splices the given item

function removeItem(id) {
  // get cart key from session storage and parse it into an object
  let cart = JSON.parse(sessionStorage.getItem('cart'));

  // loop through all items in the cart
    for (let i in cart) {
      // check if the id passed in is the same as the current item
      if (cart[i].id == id){
          // if it is, remove it, and break
        cart.splice(i, 1);
        break;
      } else {
        showCart();
      }
    }

  // add stringified cart to session storage under cart key
  sessionStorage.setItem('cart', JSON.stringify(cart));

  // call showCart again
  showCart();
}

// calculating and returning the total
function calcTotal() {
// get the value and parse from session storage
let cart = JSON.parse(sessionStorage.getItem('cart'));

// define a total variable = 0
let amount = 0;

  // loop through all items in the cart
for (let i in cart) {
  amount += cart[i].price;

}
    // add each items price to Total

  // return the total
return amount.toFixed(2);
}


// updating all classes with total being displayed
function updateTotals() {
  // define a total variable from the return of calc total
let amount = calcTotal()

  // insert that total into all places that render total
$(".total").text(`$${amount}`)

// convert total to cents
amount = amount * 100;
amount = Math.ceil(amount);

// insert form into id of pay
let html = `
<form action="/pay/?amount=${amount}" method="POST">
  <script
    src="https://checkout.stripe.com/checkout.js" class="stripe-button"
    data-key="pk_test_mVLaP8FiAKVm0TfO3eONfCrg"
    data-amount="${amount}"
    data-name="Demo Site"
    data-description="Widget"
    data-image="https://stripe.com/img/documentation/checkout/marketplace.png"
    data-locale="auto">
  </script>
</form>
`;

$('#pay').html(html);

}

function countDuplicates(id) {
  let cart = JSON.parse(sessionStorage.getItem('cart'));
  let count = 0;

  for (let i in cart) {
    if (cart[i].id == id) {
      count += 1
    }
  }

  return count;
}

// create a show cart method to render all items within the cart variable
function showCart() {
  // get the value and parse from session storage
  let cart = JSON.parse(sessionStorage.getItem('cart'));

  if (cart === null) {
    cart =[];
  }

  let cart_table = document.getElementById('cart')
  // if cart is empty, set the table in the cart col md 3 section to display none
  if (cart.length == 0) {
    cart_table.style.display = "none";
    $('#empty').text('You have no items in your cart.')
  } else {
    cart_table.style.display = "block";

    let html = '';

    let duplicates = [];

    for (let i in cart) {
      let count = countDuplicates(cart[i].id);

      if (duplicates.indexOf(cart[i].id) == -1) {
        html += `
        <tr>
          <td>${count}</td>
          <td>${cart[i].title}</td>
          <td>${(cart[i].price*count).toFixed(2)}</td>
          <td>
            <button onCLick="removeItem(${cart[i].id})" class="btn btn-danger">X</button>
          </td>
        </tr>
        `;
        duplicates.push(cart[i].id);
      }

    }

    $('tbody').html(html);
  }

  updateTotals();

  // otherwise show table by setting display to block, loop over all items in cart and create a new row for each item

  // send the proper string into the tbody section
}

showCart();

/*****************************
End cart operation functions
*****************************/
