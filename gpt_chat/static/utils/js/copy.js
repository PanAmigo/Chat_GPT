const myLink = document.getElementById('myLink') // pobierz element a
myLink.href = window.location.href // ustaw href na aktualny adres URL
myLink.textContent = window.location.href // ustaw tekst hiperłącza

const copyButton = document.getElementById('copyButton') // pobierz element przycisku
copyButton.addEventListener('click', () => {
	const tempTextarea = document.createElement('textarea') // utwórz element textarea
	tempTextarea.value = window.location.href // ustaw wartość textarea na adres URL
	document.body.appendChild(tempTextarea) // dodaj textarea do drzewa DOM
	tempTextarea.select() // zaznacz tekst w textarea
	document.execCommand('copy') // skopiuj zaznaczony tekst do schowka
	document.body.removeChild(tempTextarea) // usuń textarea z drzewa DOM
	alert('Adres URL został skopiowany do schowka!') // wyświetl komunikat o powodzeniu
})
