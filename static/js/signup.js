$(document).ready(function () {
  const $form = $('#signup-form')
  const $phoneInput = $('#phone')

  $phoneInput.on('input', function () {
    let value = $(this).val().replace(/\D/g, '')
    value = value.slice(0, 11)

    const match = value.match(/^(\d{3})(\d{4})(\d{4})$/)
    if (match) {
      $(this).val(`${match[1]}-${match[2]}-${match[3]}`)
    }
  })

  $form.on('submit', function (event) {
    event.preventDefault()

    const username = $('#username').val()
    const phone = $('#phone').val()
    const password = $('#password').val()
    const confirmPassword = $('#confirm_password').val()

    const phoneRegex = /^\d{3}-\d{4}-\d{4}$/
    if (!phoneRegex.test(phone)) {
      Swal.fire({
        title: 'ERROR',
        text: '전화번호 형식이 올바르지 않습니다.',
        icon: 'error',
        confirmButtonText: '다시 시도'
      })
      return
    }
    if (password !== confirmPassword) {
      Swal.fire({
        title: 'ERROR',
        text: '비밀번호가 서로 일치하지 않습니다.',
        icon: 'error',
        confirmButtonText: '다시 시도'
      })
      return // 함수 실행 종료
    }

    // AJAX 사용하여 서버에 데이터 전송
    $.ajax({
      url: 'api/signup',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        id_give: username,
        num_give: phone,
        pw_give: password
      }),
      success: function (data) {
        Swal.fire({
          title: 'Success',
          text: '회원가입이 완료되었습니다.',
          icon: 'success',
          confirmButtonText: '확인'
        }).then(result => {
          if (result.value) {
            window.location.href = '/login'
          }
        })
      },
      error: function (error) {
        console.error('Error:', error)
        Swal.fire({
          title: 'Error',
          text: '회원가입 중 오류가 발생했습니다.',
          icon: 'error',
          confirmButtonText: '다시 시도'
        })
      }
    })
  })
})
