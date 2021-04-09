// Get an API access token required to interact with the most of API methods.
export function getJwtToken() {
  return window.localStorage.getItem('jwt_token')
}

// Set the stored API access token to a new value.
export function setJwtToken(value) {
  return window.localStorage.setItem('jwt_token', value)
}


// A class providing methods to interact with the site API.
export class ApiClient {

  constructor (jwt_token) {
    this.jwt_token = jwt_token
  }

  get(url, data) {
    return this._makeRequest("GET", url, data)
  }

  post(url, data) {
    return this._makeRequest("POST", url, data)
  }

  _makeRequest(httpMethod, url, data, errorHandler) {
    const that = this

    let ajaxRequestOpts = {
      type: httpMethod,
      url: url,
      data: data,
      headers: {
        Authorization: 'Bearer ' + that.jwt_token
      },
      contentType : 'application/json',
      dataType: 'json',
    }

    // Set a default error handler, if `errorHandler` is not provided.
    errorHandler = errorHandler || function(xhr, textStatus, errorThrown) {
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
    }
    if (errorHandler) {
      ajaxRequestOpts["error"] = errorHandler
    }

    return $.ajax(ajaxRequestOpts)
  }
}


// Display an ERROR message to the user.
export function alertError(content) {
  _showAlert('alert-danger',   content)
}

// Display a SUCCESS message to the user.
export function alertSuccess(content) {
  _showAlert('alert-success', content)
}

function _showAlert(cls, content) {
  const alertHtml = `
  <div class="alert ${cls} alert-dismissible top fade show" role="alert">
    <div class="alert-content"> ${content} </div>
    <button type="button" class="close" data-dismiss="alert">
      <span>&times;</span>
    </button>
  </div>
  `
  $('body').prepend(alertHtml)
}


// Remove CSS classes used by Bootstrap v4 to mark form field errrors.
// `form` can be a CSS selector, a DOM element or a jQuery element.
export function clearFormErrors(form) {
  const $form = $(form)
  $form.find(".invalid-feedback").remove()
  $form.find(".is-invalid").removeClass('is-invalid')
}