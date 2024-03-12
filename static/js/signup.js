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
    const email = document.getElementById('phone').value
    const password = document.getElementById('password').value
    const confirmPassword = document.getElementById('confirm_password').value

    // 비밀번호 일치 여부  -> 이후 프론트에서 암호화해줄지 고민 필요
    if (password !== confirmPassword) {
      Swal.fire({
        title: 'ERROR',
        text: '비밀번호가 서로 일치하지 않습니다.',
        icon: 'error',
        confirmButtonText: '다시 시도'
      })
    } else {
      console.log('Username:', username)
      console.log('Email:', email)
      console.log('Password:', password)
      console.log('Confirm Password:', confirmPassword)
      //   form.submit() // 폼 제출을 진행하려면 이 주석을 해제하세요.
    }
  })
})
