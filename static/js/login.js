document.addEventListener('DOMContentLoaded', function () {
  // 폼 제출 이벤트 핸들러
  const form = document.getElementById('login-form')
  form.addEventListener('submit', function (event) {
    event.preventDefault()
    const username = document.getElementById('username').value
    const password = document.getElementById('password').value
    // AJAX 사용하여 서버에 데이터 전송
    $.ajax({
      url: 'api/login',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        id_give: username,
        pw_give: password
      }),
      success: function (data) {
        console.log('Success:', data)
        // cookie에 저장

        Swal.fire({
          title: 'Success',
          text: '로그인 완료되었습니다.',
          icon: 'success',
          confirmButtonText: '확인'
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
    }) // AJAX call 닫음
  }) // form eventListener 닫음
}) // DOMContentLoaded eventListener 닫음
