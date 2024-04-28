const expandBtn = document.getElementById('expand-button');
const additionalDtls = document.getElementById('additional-details');

expandBtn.addEventListener('click', () => {
    additionalDtls.classList.toggle('hidden');

    expandBtn.textContent = additionalDtls.classList.contains('hidden') ? '▼' : '▲';
});