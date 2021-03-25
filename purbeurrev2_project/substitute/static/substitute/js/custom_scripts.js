$('.save-button').on('click', function(event) {
  let cookie = document.cookie
  let csrfToken = cookie.substring(cookie.indexOf('=') + 1)
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
    alert(response.message);
    if (response.allowed) {
      $button.prop("disabled", true);
    }
  });
});
