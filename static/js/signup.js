// document
//   .getElementById('signup-form')
//   .addEventListener('submit', function (event) {
//     event.preventDefault() // 폼 제출을 막음

//     Swal.fire({
//       title: '회원가입 성공!',
//       text: '가입을 환영합니다.',
//       icon: 'success',
//       confirmButtonText: '좋아요'
//     }).then(result => {
//       if (result.isConfirmed) {
//         this.submit() // 실제 폼 제출
//       }
//     })
//   })

document.addEventListener('DOMContentLoaded', function () {
  document
    .getElementById('signup-form')
    .addEventListener('submit', function (event) {
      event.preventDefault() // 폼의 기본 제출 동작을 막습니다.

      // 각 입력 필드에서 값을 가져옵니다.
      var username = document.getElementById('username').value
      var email = document.getElementById('email').value
      var password = document.getElementById('password').value
      var confirmPassword = document.getElementById('confirm_password').value

      // 콘솔에 값 출력
      console.log('Username:', username)
      console.log('Email:', email)
      console.log('Password:', password)
      console.log('Confirm Password:', confirmPassword)

      // 여기에 폼 제출에 대한 추가 처리 로직을 추가할 수 있습니다.
    })
})
