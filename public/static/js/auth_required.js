(async () =>{
    const result = await fetch("/auth")
    if (!result.ok) {
        window.location.href = `/signin`
        location.reload()
        return
    }
    return
})()