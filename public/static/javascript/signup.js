const profileImgInput = document.getElementById("profile-img-input")
const profileImgBtn = document.getElementById("profile-img-btn")

const btn_without_file_content = `
    <p class="page-title text-lg font-normal text-gray-900">Add photo</p>
    <img class="h-7" src="/static/svg/add_photo.svg" alt="add_photo">
`
const btn_with_file_content = `
    <p class="page-title text-lg font-normal text-gray-900">File selected</p>
`
profileImgBtn.addEventListener('click', () => {
    profileImgInput.click()
})

profileImgInput.addEventListener('change', (event) => {
    if (event.target.files.length === 0) {
        profileImgBtn.innerHTML = btn_without_file_content
    } else if (event.target.files.length === 1) {
        profileImgBtn.innerHTML = btn_with_file_content
    }
})


