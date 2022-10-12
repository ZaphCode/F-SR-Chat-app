const profileImgInput = document.getElementById("profile-img-input")
const profileImgBtn = document.getElementById("profile-img-btn")

const btn_without_file_content = `
    <p class="font-normal text-gray-500">Add photo</p>
    <ion-icon name="image-outline" class="text-xl text-gray-500"></ion-icon>
`
const btn_with_file_content = `
    <p class="font-normal text-gray-500">File selected</p>
    <ion-icon name="checkmark-circle-outline" class="text-xl text-gray-500"></ion-icon>
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


