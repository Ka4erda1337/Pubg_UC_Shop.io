// script.js

const catalog = [
  {name: '60 UC', price: '50 ₽', img: 'images/uc60.png'},
  {name: '300 UC', price: '250 ₽', img: 'images/uc300.png'},
  {name: '1500 UC', price: '1200 ₽', img: 'images/uc1500.png'},
  {name: '4000 UC', price: '3200 ₽', img: 'images/uc4000.png'}
];

const catalogEl = document.getElementById('catalog');

function renderCatalog() {
  catalog.forEach(item => {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <img src="${item.img}" alt="${item.name}">
      <h2>${item.name}</h2>
      <p class="price">${item.price}</p>
      <button onclick="buy('${item.name}')">Купить</button>
    `;
    catalogEl.appendChild(card);
  });
}

renderCatalog();

const modal = document.getElementById('modal');
const modalTitle = document.getElementById('modalTitle');
const modalMeta = document.getElementById('modalMeta');
const confirmBuy = document.getElementById('confirmBuy');
const cancelBuy = document.getElementById('cancelBuy');
const closeModal = document.getElementById('closeModal');

function buy(itemName) {
  modal.classList.add('show');
  modalMeta.textContent = `Вы выбираете: ${itemName}`;
}

confirmBuy.onclick = () => {
  alert('Покупка подтверждена!');
  modal.classList.remove('show');
};

cancelBuy.onclick = closeModal.onclick = () => {
  modal.classList.remove('show');
};
