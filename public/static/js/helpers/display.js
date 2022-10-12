export class DisplayManager {
    constructor(MC) {
        this.MC = MC;
    }

    messageContainerComponent() {
        return `
        <div class="flex flex-col-reverse pt-10 msg-div pr-3 gap-y-2 overflow-y-scroll h-full w-full">
            <div id="no-msg" class="flex justify-center">
                <p>No messages to display</p>
            </div>
        </div>
        <div id="msg-header" class="absolute bg-gray-100 top-0 w-full -ml-3 flex justify-center">
            <h3 class="title font-semibold text-center py-3 w-1/3 text-gray-700"></h3>
        </div>
        <form id="msg-form" class="h-15 mt-7 relative flex justify-center">
            <div id="emojis-div" class="bg-gray-100 shadow-lg hidden grid-cols-3 z-50 shadow-gray-400 w-40 right-5 lg:right-7 xl:right-12 bottom-20 h-32 absolute">
                <p class="emoji cursor-pointer text-center m-2">😁</p>
                <p class="emoji cursor-pointer text-center m-2">😎</p>
                <p class="emoji cursor-pointer text-center m-2">🥰</p>
                <p class="emoji cursor-pointer text-center m-2">😡</p>
                <p class="emoji cursor-pointer text-center m-2">😢</p>
                <p class="emoji cursor-pointer text-center m-2">😂</p>
                <p class="emoji cursor-pointer text-center m-2">👌</p>
                <p class="emoji cursor-pointer text-center m-2">❤️</p>
                <p class="emoji cursor-pointer text-center m-2">🤖</p>
            </div>
            <input id="msg-input" name="msg-input" autocomplete="off" class="text-black px-5 py-3 outline-none w-3/4" type="text" placeholder="Send message"/>
            <ion-icon name="happy" id="emojis-btn" class="px-3 flex items-center text-lg cursor-pointer py-4 bg-white text-gray-600"></ion-icon>
            <button type="submit" class="px-3 flex items-center text-lg bg-white text-gray-600"><ion-icon name="paper-plane-sharp"></ion-icon></button>
        </form>`
    }

    messageComponent(msg, you, him) {
        const container = document.createElement('div')
        container.classList.add("flex", "gap-x-3")
        const text = document.createElement('p')
        text.classList.add("max-w-xxs", "sm:max-w-xs", "md:max-w-sm", "overflow-clip", "text-white", "py-2", "px-4")
        const image = document.createElement('img')
        image.classList.add("w-8", "h-8", "rounded-full", "object-cover")
        text.innerText = msg.message
        if (msg.sender_pk === you.pk) {
            container.classList.add("justify-end")
            text.classList.add("bg-gray-700")
            if (you.image_url) image.src = you.image_url
            else image.src = "/static/default_profile.jpg"
            container.appendChild(text)
            container.appendChild(image)
        } else {
            container.classList.add("justify-start")
            text.classList.add("bg-gray-500")
            if (him.image_url) image.src = him.image_url
            else image.src = "/static/default_profile.jpg"
            container.appendChild(image)
            container.appendChild(text)
        }

        return container
    }

    renderNewMessage(msg, you, him) {
        const no_msg = document.getElementById("no-msg")
        if (no_msg) no_msg.remove()
        const message = this.messageComponent(msg, you, him)
        this.MC.firstElementChild.insertBefore(message, this.MC.firstElementChild.firstChild)
    }

    renderLoading() {
        this.MC.innerHTML = `
        <div class="flex flex-col items-center gap-2 justify-center h-full w-full">
            <ion-icon class="-mt-10 loading-spinner text-3xl text-gray-400" name="sync-outline"></ion-icon>
        </div>`
    }

    renderError(msg) {
        this.MC.innerHTML = `
        <div class="flex flex-col items-center gap-2 justify-center h-full w-full">
            <ion-icon class=" text-6xl text-gray-600" name="sad-outline"></ion-icon>
            <h3 class="text-gray-600 title font-semibold text-lg text-center text-clip">Something went wrong</h3>
            <p class="text-gray-500 max-w-xs text-center text-clip">${msg}</p>
        </div>`
    }

    renderMessages(messages, you, him) {
        this.MC.innerHTML = this.messageContainerComponent()
        document.getElementById("msg-header").firstElementChild.innerText = him.username

        if (messages.length === 0) return

        const no_msg = document.getElementById("no-msg")
        if (no_msg) no_msg.remove()

        for (let msg of messages) {
            let message = this.messageComponent(msg, you, him)
            this.MC.firstElementChild.append(message)
        }
    }

    renderMoreMessages(messages, you, him) {
        for (let msg of messages) {
            let message = this.messageComponent(msg, you, him)
            this.MC.firstElementChild.append(message)
        }
    }
}

