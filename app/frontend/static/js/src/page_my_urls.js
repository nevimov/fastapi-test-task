import { ApiClient, alertSuccess, alertError, getJwtToken, clearFormErrors } from './utils'

;(function() {
  const urls = window.urls

  // The code in this module is specific to the "My URLs" page
  if (window.location.href !== urls.pages.MY_URLS) {
    return
  }

  // If the user is not authenticated, redirect him to the login page.
  const jwt_token = getJwtToken()
  if (!jwt_token) {
    window.location.replace(urls.pages.LOGIN)
  }

  const apiClient = new ApiClient(jwt_token)


  // ***************************
  // *** Paginated URL Table ***
  // ***************************

  const URLS_PER_PAGE = 25

  const $urlTableSpinner = $('#my-urls-table-spinner')
  const $urlTableBody = $('#my-urls-table tbody')
  const $urlPagination = $('#my-urls-pagination')


  // Display user URLs
  function displayUrls(skip, limit) {
    skip = skip || 0
    limit = limit || URLS_PER_PAGE

    $urlTableSpinner.show()

    const xhr = apiClient.get(
      urls.api.GET_MY_URLS,
      {skip: skip, limit: limit}
    )

    xhr.done(function (data, textStatus, xhr) {
      const urls = data
      // Populate the URL table
      for (let i = 0; i < urls.length; i++) {
        const url = urls[i]
        const shortUrl = `${location.protocol}//${location.host}/${url.key}`
        const originalUrl = url.destination
        $urlTableBody.append(`
          <tr>
            <td>${i+1}</td>
            <td><a href="${originalUrl}">${originalUrl}</a></td>
            <td><a href="${shortUrl}">/${url.key}</td>
          </tr>
        `)
      }
      createPagination(xhr)
    })

    xhr.fail(function(xhr, textStatus, errorThrown) {
      if (xhr.readyState !== 4) {
        return
      }
      const errorMsg = xhr.responseJSON["detail"]
      alertError(errorMsg)
    })

    xhr.always(function (xhr, textStatus) {
      $urlTableSpinner.hide()
    })
  }


  // Clear the URL table
  function clearUrls() {
    $urlTableBody.empty()
  }


  // Function to run when a pagination link is clicked
  function changeUrlsPage(event) {
    clearUrls()
    displayUrls(event.data.skip, URLS_PER_PAGE)
  }

  // Create (or recreate) pagination links for the URL table
  function createPagination(xhr) {
    $urlPagination.empty()
    const totalUrlCount = xhr.getResponseHeader('X-User-Url-Count')
    const pageCount = Math.ceil(totalUrlCount / URLS_PER_PAGE)
    for (let i = 1; i <= pageCount; i++) {
      const $link = $(
        `<li class="page-item"> <a href="#!" class="page-link">${i}</a> </li>`
      )
      $link.on("click", {skip: (i - 1) * URLS_PER_PAGE}, changeUrlsPage)
      $urlPagination.append($link)
    }
  }


  // Init. Display the first page.
  displayUrls()


  // ******************************
  // *** "Add a Short URL" Form ***
  // ******************************

  $("#add-url-form").on("submit", function (event) {
    event.preventDefault()
    const form = this

    if (form.checkValidity() === false) {
      return
    }

    const $form = $(form)
    const redirectTo = $form.find('[name="destination"]').val()
    const redirectFrom = $form.find('[name="key"]').val()
    let requestData = {
      "destination": redirectTo,
    }
    if (redirectFrom) {
      requestData["key"] = redirectFrom
    }
    requestData = JSON.stringify(requestData)
    const xhr = apiClient.post(urls.api.ADD_URL, requestData)

    xhr.done(function (data, status, xhr) {
      clearFormErrors($form)
      clearUrls()
      displayUrls()
      createPagination(xhr)
      const longUrlLink = `<a href="${data['destination']}">${data['destination']}</a>`
      const shortUrl = `${location.protocol}//${location.host}/${data["key"]}`
      const shortUrlLink = `<a href="${shortUrl}">${shortUrl}</a>`
      alertSuccess(`Success! Created redirect from ${shortUrlLink} to ${longUrlLink}.`)
    })

    xhr.fail(function(xhr, textStatus, errorThrown) {
      if (xhr.readyState !== 4) {
        return
      }

      clearFormErrors($form)
      const errDetail = xhr.responseJSON["detail"]
      if (typeof errDetail === "string") {
        alertError(`${errDetail}`)
        return
      }
      for (let i = 0; i < errDetail.length; i++) {
        const error = errDetail[i]
        const fieldName = error["loc"][1]
        const $field = $form.find(`[name="${fieldName}"]`)
        $field.addClass("is-invalid")
        $field.parent().append(`<div class="invalid-feedback">${error["msg"]}</div>`)
      }
    })

  })

  console.log('done')
})()
