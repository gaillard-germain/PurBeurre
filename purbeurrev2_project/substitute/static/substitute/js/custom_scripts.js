let cookie = document.cookie
let csrfToken = cookie.substring(cookie.indexOf('=') + 1)


$('.save-button').on('click', function(event) {
  $button = $(this)
  var id = $button.val();
  $.ajax({
    url: '/substitute/addfav/',
    headers: {
           'X-CSRFToken': csrfToken
         },
    data: {
      product_id: id
    },
    type: 'POST'
  })
  .done(function(response) {
    if (response.message) {
      alert(response.message);
    }
    if (response.allowed) {
      location.reload();
    }
  });
});

$('.remove-button').on('click', function(event) {
  $button = $(this)
  var id = $button.val();
  $.ajax({
    url: '/substitute/removefav/',
    headers: {
           'X-CSRFToken': csrfToken
         },
    data: {
      product_id: id
    },
    type: 'POST'
  })
  .done(function(response) {
    if (response.message) {
      alert(response.message);
    }
    if (response.allowed) {
      location.reload();
    }
  });
});
