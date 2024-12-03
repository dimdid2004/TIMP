let isProtected = false
const passwordHash =
	'8e67dd1355714239acde098b6f1cf906bde45be6db826dc2caca7536e07ae844' // Захешированный пароль secret_password

document
	.getElementById('enableProtection')
	.addEventListener('click', enableProtection)
document
	.getElementById('disableProtection')
	.addEventListener('click', disableProtection)

function enableProtection() {
	if (!isProtected) {
		document.body.classList.add('protected')
		//disableShortcuts();
		// Запрет на правый клик мышью
		document.addEventListener('contextmenu', disableContextMenu)
		// Запрет на Ctrl+C
		document.addEventListener('keydown', disableCtrlC)
		// Что-то похожее на запрет Print-screen
		document.addEventListener('keyup', disablePrtScr)

		isProtected = true
		alert('Защита включена')
	}
}

async function disableProtection() {
	const userPassword = prompt('Введите пароль для отключения защиты:')

	// Используем await для получения хэша пароля
	const userPasswordHash = await getSha256Hash(userPassword)

	if (userPasswordHash === passwordHash) {
		document.body.classList.remove('protected')
		document.removeEventListener('contextmenu', disableContextMenu)
		document.removeEventListener('keydown', disableCtrlC)
		document.removeEventListener('keyup', disablePrtScr)
		isProtected = false
		let protectedElement = document.querySelector('#content')
		if (protectedElement.classList.contains('hidden')) {
			protectedElement.classList.remove('hidden')
		}

		let infMessage = document.querySelector('#protection-from-shortcutting')
		if (!infMessage.classList.contains('hidden')) {
			infMessage.classList.add('hidden')
		}
		alert('Защита отключена')
	} else {
		alert(`Неверный пароль`)
	}
}

async function sha256_hash(text) {
	const msgUint8 = new TextEncoder().encode(text) // encode as (utf-8) Uint8Array
	const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8) // hash the message
	const hashArray = Array.from(new Uint8Array(hashBuffer)) // convert buffer to byte array
	const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('') // convert bytes to hex string
	return hashHex
}

async function getSha256Hash(text) {
	return await sha256_hash(text)
}

function disablePrtScr(event) {
	if (event.key === 'PrintScreen') {
		hideProtectedText()
	}
}

function enableShortcuts() {
	document.removeEventListener('contextmenu', disableContextMenu)
	document.removeEventListener('keydown', disableCtrlC)
}

function disableContextMenu(event) {
	event.preventDefault()
}

function disableCtrlC(event) {
	if (event.ctrlKey && event.key.toLowerCase() === 'c') {
		event.preventDefault()
		alert('Повторяю, вы не можете копировать!')
	}
}

function hideProtectedText() {
	let protectedElement = document.querySelector('#content')
	let infMessage = document.querySelector('#protection-from-shortcutting')

	protectedElement.classList.add('hidden')
	infMessage.classList.remove('hidden')
}
