function toggleCardFields() {
    const method = document.getElementById('payment-method').value;
    document.getElementById('card-fields').style.display = method === 'card' ? 'block' : 'none';
}