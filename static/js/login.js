$(document).ready(function () {
  $('#login-form').on('submit', function (event) {
    event.preventDefault()
    const username = $('#username').val()
    const password = $('#password').val()
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
        if (data.result === 'fail') {
          Swal.fire({
            title: 'Error',
            text: '아이디 또는 비밀번호가 일치하지 않습니다.',
            icon: 'error',
            confirmButtonText: '다시 시도'
          })
          return
        }
        // 로그인 성공: 사용자가 '확인'을 클릭하면 /posts 페이지로 리디렉션
        Swal.fire({
          title: 'Success',
          text: '로그인 완료되었습니다.',
          icon: 'success',
          confirmButtonText: '확인'
        }).then(result => {
          if (result.value) {
            window.location.href = '/posts'
          }
        })
      },
      error: function (error) {
        console.error('Error:', error)
        Swal.fire({
          title: 'Error',
          text: '로그인 중 오류가 발생했습니다.',
          icon: 'error',
          confirmButtonText: '다시 시도'
        })
      }
    })
  })
})
