const getToken = (name) => {
	let cookieValue = null
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';')
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim()
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === name + '=') {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
				break
			}
		}
	}
	return cookieValue
}

const csrftoken = getToken('csrftoken')

const addCartDOMs = document.getElementsByClassName('add-cart-btn')

for (btn of addCartDOMs) {
	btn.addEventListener('click', (e) => {
		console.log('Adding')
		const productId = e.target.dataset.product

		const url = `http://127.0.0.1:8000/carts/api/add_cart/${productId}/`

		fetch(url, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': csrftoken,
			},
			body: JSON.stringify({
				quantity: 1,
			}),
		})
			.then((response) => {
				return response.json()
			})
			.then((data) => {
				console.log('data: ', data)
				window.location.reload()
			})
	})
}

const quantityInputDOMs = document.getElementsByClassName('cart-item-quantity')
const updateCartDOM = $('.update-cart-btn').on('click', async () => {
	const url = `http://127.0.0.1:8000/carts/api/update_cart/`

	const requestBody = [...quantityInputDOMs]
		.filter((btn) => btn.dataset.cart_item)
		.map((btn) => {
			if (!btn.dataset.cart_item) return
			return {
				cart_item_id: btn.dataset.cart_item,
				quantity: btn.value,
			}
		})

	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({
			...requestBody
		}),
	})
		.then((response) => {
			return response.json()
		})
		.then((data) => {
			console.log('data: ', data)
			window.location.reload()
		})
})
