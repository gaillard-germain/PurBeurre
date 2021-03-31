let csrfToken = $("[name=csrfmiddlewaretoken]").val();

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
    if (response.allowed) {
      location.reload();
    }else {
      alert("Veuillez vous connecter SVP");
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
