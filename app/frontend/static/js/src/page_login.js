import { alertError, setJwtToken } from './utils'

;(function() {
  const urls = window.urls

  $("#login-form").on("submit", function (event) {
    event.preventDefault()
    const form = this

    if (form.checkValidity() === false) {
      return
    }

    const $form = $(form)
    const postUrl = $form.attr('action')
    const postData = $form.serialize()

    $.post(postUrl, postData)
      .done(function(data) {
        // On success, save the token and redirect the user to the "My URLs" page
        setJwtToken(data["access_token"])
        window.location.href = urls.pages.MY_URLS
      })
      .fail(function(xhr, textStatus, errorThrown) {
        if (xhr.readyState == 0) {
          // Network error (connection refused, access denied due to CORS, etc.)
          alertError(
            "Can't connect with the server. " +
            "Please check your network connection or try again later."
          )
        }
        else if (xhr.readyState < 4) {
          // Something weird is happening
          alertError("An unknown error occurred. Please try again later.")
        }
        else {
          const errorMsg = xhr.responseJSON["detail"]
          alertError(errorMsg)
        }
      })

  })
})()
