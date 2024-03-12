document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('signup-form')
  const phoneInput = document.getElementById('phone')

  // 전화번호 입력시 하이픈 추가 로직
  phoneInput.addEventListener('input', function (e) {
    let value = this.value.replace(/\D/g, '')
    value = value.slice(0, 11)

    const match = value.match(/^(\d{0,3})(\d{0,4})(\d{0,4})$/)
    if (match) {
      this.value = `${match[1]}${match[2] ? '-' : ''}${match[2]}${
        match[3] ? '-' : ''
      }${match[3]}`
    }
  })

  // 폼 제출 이벤트 핸들러
  form.addEventListener('submit', function (event) {
    event.preventDefault()

    const username = document.getElementById('username').value
    const phone = document.getElementById('phone').value
    const password = document.getElementById('password').value
    const confirmPassword = document.getElementById('confirm_password').value

    // 비밀번호 일치 여부 검사
    if (password !== confirmPassword) {
      Swal.fire({
        title: 'ERROR',
        text: '비밀번호가 서로 일치하지 않습니다.',
        icon: 'error',
        confirmButtonText: '다시 시도'
      })
    } else {
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
          console.log('Success:', data)
          Swal.fire({
            title: 'Success',
            text: '회원가입이 완료되었습니다.',
            icon: 'success',
            confirmButtonText: '확인'
          })
          // 로그인 페이지로 리다이렉션
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
    }
  })
})
