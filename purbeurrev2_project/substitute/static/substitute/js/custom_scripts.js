let cookie = document.cookie
let csrfToken = cookie.substring(cookie.indexOf('=') + 1)

$.fn.toggleFav = function(toggle, id) {
  $.ajax({
    url: '/substitute/togglefav/',
    headers: {
           'X-CSRFToken': csrfToken
         },
    data: {
      toggle: toggle,
      product_id: id
    },
    type: 'POST'
  })
  .done(function(response) {
    if (response.message != 'OK') {
      alert(response.message);
    }
    if (response.allowed) {
      location.reload();
    }
  });
}

$('.add-fav').on('click', function(event) {
  var id = $(this).val();
  $.fn.toggleFav("on", id);
});

$('.remove-fav').on('click', function(event) {
  var id = $(this).val();
  $.fn.toggleFav("off", id);
});
