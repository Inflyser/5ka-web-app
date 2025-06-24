function renderCategories(rawCategories) {
    const listElem = document.getElementById('categoriesList');
    listElem.innerHTML = ''; // Очистить

    if (!rawCategories || rawCategories.length === 0) {
        listElem.innerHTML = '<li>Категории не найдены</li>';
        return;
    }

    rawCategories.forEach(parent => {
        const parentName = parent.name || 'Без названия';
        const parentId = parent.id;

        const parentLi = document.createElement('li');
        parentLi.innerHTML = `<strong>${parentName}</strong> (ID: ${parentId})`;
        listElem.appendChild(parentLi);

        const subUl = document.createElement('ul');

        parent.categories.forEach(sub => {
            const subLi = document.createElement('li');
            subLi.innerHTML = `
                <span>${sub.name}</span><br>
                <img src="${sub.image_link}" alt="${sub.name}" width="50"><br>
                <small style="color:${sub.title_color}">ID: ${sub.id}</small>
            `;

            subUl.appendChild(subLi);
        });

        listElem.appendChild(subUl);
    });
}


document.addEventListener("DOMContentLoaded", () => {
    const rawCategories = JSON.parse(localStorage.getItem('categories'));
    renderCategories(rawCategories);
});