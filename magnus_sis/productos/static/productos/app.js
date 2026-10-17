(() => {
  'use strict';

  const PRODUCT_KEY = 'magnusSIS.products.v1';
  const CATEGORY_KEY = 'magnusSIS.categories.v1';
  const LOW_STOCK = 5;
  const PAGE_SIZE = 5;
  const path = window.location.pathname;

  function read(key) {
    try {
      const value = JSON.parse(localStorage.getItem(key) || '[]');
      return Array.isArray(value) ? value : [];
    } catch (_) {
      return [];
    }
  }

  function write(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (_) {
      alert('No se pudieron guardar los cambios en este navegador. Revisa el espacio disponible o la configuración de almacenamiento.');
      return false;
    }
  }

  let products = read(PRODUCT_KEY);
  let categories = read(CATEGORY_KEY);

  const byId = (id) => document.getElementById(id);
  const money = (value) => '$ ' + Number(value || 0).toLocaleString('es-CO');
  const makeId = () => (window.crypto && crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`);
  const nextProductId = () => String(products.reduce((max, product) => Math.max(max, Number(product.id) || 0), 0) + 1);
  const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
  const fmtDate = (value) => value ? new Intl.DateTimeFormat('es-CO', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value)) : '—';
  const stockState = (product) => Number(product.quantity) <= 0 ? 'out' : Number(product.quantity) <= LOW_STOCK ? 'low' : 'ok';
  const statusLabel = (product) => ({ ok: 'Disponible', low: 'Stock bajo', out: 'Agotado' })[stockState(product)];
  const productUrl = (id, action = '') => `/productos/${encodeURIComponent(id)}/${action}`;

  function categoryName(id) {
    return categories.find((category) => category.id === id)?.name || 'Sin categoría';
  }

  function refreshStats() {
    if (byId('stat-products')) byId('stat-products').textContent = products.length;
    if (byId('stat-categories')) byId('stat-categories').textContent = categories.length;
    const lowStockCount = products.filter((product) => stockState(product) === 'low').length;
    if (byId('stat-low-stock')) {
      byId('stat-low-stock').textContent = lowStockCount;
      byId('stat-low-stock').closest('.stat')?.classList.toggle('attention', lowStockCount > 0);
    }
  }

  function renderProductList() {
    const tbody = byId('product-rows');
    if (!tbody) return;

    const searchField = byId('product-search');
    const search = (searchField ? searchField.value : new URLSearchParams(location.search).get('q') || '').trim().toLocaleLowerCase('es');
    const categoryFilter = byId('filter-category')?.value || new URLSearchParams(location.search).get('categoria') || '';
    const stockFilter = byId('filter-stock')?.value || '';
    const filtered = products.filter((product) => {
      const matchesSearch = !search || `${product.name} ${product.description || ''}`.toLocaleLowerCase('es').includes(search);
      const matchesCategory = !categoryFilter || product.categoryId === categoryFilter;
      const matchesStock = !stockFilter || stockState(product) === stockFilter;
      return matchesSearch && matchesCategory && matchesStock;
    });

    const pageCount = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
    let page = Math.min(Number(sessionStorage.getItem('magnusSIS.productPage') || 1), pageCount);
    const pageItems = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);
    const empty = byId('product-empty');
    const table = byId('products-table');
    const pagination = byId('product-pagination');

    if (!filtered.length) {
      empty.hidden = false;
      empty.querySelector('h2').textContent = products.length
        ? 'No encontramos productos'
        : categories.length
          ? 'Aún no hay productos'
          : 'Empieza por crear una categoría';
      empty.querySelector('p').textContent = products.length
        ? 'Prueba con otra búsqueda o cambia los filtros.'
        : categories.length
          ? 'Tu inventario ya tiene categorías. Registra el primer producto para empezar.'
          : 'Crea una categoría para organizar el inventario antes de registrar productos.';
      empty.querySelector('a').hidden = products.length > 0;
      if (!products.length) {
        const firstAction = empty.querySelector('a');
        firstAction.href = categories.length ? '/productos/nuevo/' : '/categorias/';
        firstAction.textContent = categories.length ? 'Nuevo producto' : 'Crear primera categoría';
      }
      table.hidden = true;
      pagination.hidden = true;
    } else {
      empty.hidden = true;
      table.hidden = false;
      pagination.hidden = false;
      tbody.innerHTML = pageItems.map((product) => {
        const state = stockState(product);
        return `<tr>
          <td><div class="product"><span><b>${escapeHtml(product.name)}</b><small>SKU · ${escapeHtml(product.sku || '—')}</small></span></div></td>
          <td>${escapeHtml(categoryName(product.categoryId))}</td><td>${money(product.price)}</td><td>${Number(product.quantity)} un.</td>
          <td><span class="badge ${state}">${statusLabel(product)}</span></td>
          <td><div class="actions"><a class="table-action" href="${productUrl(product.id)}" aria-label="Ver ${escapeHtml(product.name)}">Ver</a><a class="table-action" href="${productUrl(product.id, 'editar/')}" aria-label="Editar ${escapeHtml(product.name)}">Editar</a><a class="table-action danger-text" href="${productUrl(product.id, 'eliminar/')}" aria-label="Eliminar ${escapeHtml(product.name)}">Eliminar</a></div></td>
        </tr>`;
      }).join('');
      byId('product-count').textContent = `Mostrando ${(page - 1) * PAGE_SIZE + 1}–${Math.min(page * PAGE_SIZE, filtered.length)} de ${filtered.length} productos`;
      const pageNav = byId('product-pages');
      pageNav.innerHTML = `<button type="button" data-page="${page - 1}" ${page === 1 ? 'disabled' : ''}>Anterior</button>${Array.from({ length: pageCount }, (_, index) => `<button type="button" data-page="${index + 1}" class="${page === index + 1 ? 'chosen' : ''}" ${page === index + 1 ? 'aria-current="page"' : ''}>${index + 1}</button>`).join('')}<button type="button" data-page="${page + 1}" ${page === pageCount ? 'disabled' : ''}>Siguiente</button>`;
      pageNav.querySelectorAll('[data-page]').forEach((button) => button.addEventListener('click', () => {
        sessionStorage.setItem('magnusSIS.productPage', String(Number(button.dataset.page)));
        renderProductList();
      }));
    }

    refreshStats();
  }

  function setupProductList() {
    const categorySelect = byId('filter-category');
    if (!categorySelect) return;
    const selected = new URLSearchParams(location.search).get('categoria') || '';
    categorySelect.innerHTML = '<option value="">Todas las categorías</option>' + categories.map((category) => `<option value="${escapeHtml(category.id)}">${escapeHtml(category.name)}</option>`).join('');
    categorySelect.value = selected;
    const searchField = document.querySelector('form.toolbar input[name="q"]');
    if (searchField) {
      searchField.id = 'product-search';
      searchField.value = new URLSearchParams(location.search).get('q') || '';
      searchField.addEventListener('input', () => { sessionStorage.setItem('magnusSIS.productPage', '1'); renderProductList(); });
      searchField.form.addEventListener('submit', (event) => event.preventDefault());
    }
    categorySelect.addEventListener('change', () => { sessionStorage.setItem('magnusSIS.productPage', '1'); renderProductList(); });
    byId('filter-stock').addEventListener('change', () => { sessionStorage.setItem('magnusSIS.productPage', '1'); renderProductList(); });
    renderProductList();
  }

  function setupProductForm(editId) {
    const form = byId('product-form');
    if (!form) return;
    const categoryField = byId('categoria');
    const product = editId ? products.find((item) => item.id === editId) : null;
    if (editId && !product) {
      form.closest('.form-layout').innerHTML = '<div class="empty-state card" role="status"><h2>Producto no encontrado</h2><p>Puede que haya sido eliminado.</p><a class="btn primary" href="/">Volver al inventario</a></div>';
      return;
    }
    categoryField.innerHTML = '<option value="">Selecciona una categoría</option>' + categories.map((category) => `<option value="${escapeHtml(category.id)}">${escapeHtml(category.name)}</option>`).join('');
    if (product) {
      byId('nombre').value = product.name;
      byId('categoria').value = product.categoryId;
      byId('precio').value = product.price;
      byId('cantidad').value = product.quantity;
      byId('descripcion').value = product.description || '';
      document.querySelector('.preview-box b').textContent = product.name;
      document.querySelector('.preview-box small').textContent = categoryName(product.categoryId);
    }
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      if (!categories.length) {
        alert('Primero crea una categoría para clasificar el producto.');
        location.href = '/categorias/';
        return;
      }
      const now = new Date().toISOString();
      const item = {
        id: product?.id || nextProductId(),
        sku: product?.sku || `PRD-${nextProductId().padStart(4, '0')}`,
        name: byId('nombre').value.trim(),
        categoryId: categoryField.value,
        price: Number(byId('precio').value),
        quantity: Number(byId('cantidad').value),
        description: byId('descripcion').value.trim(),
        createdAt: product?.createdAt || now,
        updatedAt: now,
      };
      if (!item.name || !item.categoryId || item.price <= 0 || item.quantity < 0) {
        alert('Revisa los campos: el nombre y la categoría son obligatorios, el precio debe ser mayor que cero y la cantidad no puede ser negativa.');
        return;
      }
      const next = product ? products.map((entry) => entry.id === product.id ? item : entry) : [...products, item];
      if (write(PRODUCT_KEY, next)) location.href = '/';
    });
  }

  function setupDetail(id) {
    const product = products.find((item) => item.id === id);
    if (!product) {
      byId('product-detail').hidden = true;
      byId('detail-missing').hidden = false;
      return;
    }
    const state = stockState(product);
    byId('detail-crumb').textContent = product.name;
    byId('detail-name').textContent = product.name;
    byId('detail-sku').textContent = product.sku || '—';
    byId('detail-category').textContent = categoryName(product.categoryId);
    byId('detail-price').textContent = `${money(product.price)} COP`;
    byId('detail-quantity').textContent = `${product.quantity} unidades`;
    byId('detail-id').textContent = product.sku || '—';
    byId('detail-created').textContent = fmtDate(product.createdAt);
    byId('detail-updated').textContent = fmtDate(product.updatedAt);
    byId('detail-description').textContent = product.description || 'Sin descripción.';
    byId('detail-status').textContent = statusLabel(product);
    byId('detail-status').className = `badge ${state}`;
    byId('detail-stock-number').textContent = product.quantity;
    byId('detail-stock-caption').textContent = state === 'out' ? 'Producto agotado' : state === 'low' ? 'Nivel de stock bajo' : 'Nivel de stock adecuado';
    byId('detail-stock-track').style.width = `${Math.min(100, Math.max(0, Number(product.quantity) * 5))}%`;
    byId('detail-stock-track').style.background = state === 'out' ? '#bf3d43' : state === 'low' ? '#e1a238' : '#44ae83';
    byId('detail-edit').href = productUrl(product.id, 'editar/');
    byId('detail-delete').href = productUrl(product.id, 'eliminar/');
  }

  function setupDelete(id) {
    const product = products.find((item) => item.id === id);
    if (!product) {
      byId('delete-stage').hidden = true;
      byId('delete-missing').hidden = false;
      return;
    }
    byId('delete-name').textContent = product.name;
    byId('delete-meta').textContent = `${categoryName(product.categoryId)} · ${money(product.price)} COP · ${product.quantity} unidades`;
    byId('confirm-delete').addEventListener('click', () => {
      if (write(PRODUCT_KEY, products.filter((entry) => entry.id !== product.id))) location.href = '/';
    });
  }

  function showCategoryDialog(category = null) {
    const dialog = document.createElement('dialog');
    dialog.className = 'category-dialog';
    dialog.setAttribute('aria-labelledby', 'category-dialog-title');
    dialog.setAttribute('aria-describedby', 'category-dialog-description');
    dialog.innerHTML = `<form method="dialog" class="category-dialog-card">
      <div class="dialog-heading"><div><h2 id="category-dialog-title">${category ? 'Editar categoría' : 'Nueva categoría'}</h2><p id="category-dialog-description">Agrupa productos con características similares.</p></div></div>
      <label class="field"><span>Nombre de la categoría <span class="required">*</span></span><input name="name" maxlength="100" required value="${escapeHtml(category?.name || '')}" placeholder="Ej. Periféricos" aria-describedby="category-name-error"><span class="field-error" id="category-name-error" role="alert" hidden></span></label>
      <label class="field"><span>Descripción <span class="optional">Opcional</span></span><textarea name="description" maxlength="300" placeholder="Qué tipo de productos pertenecen aquí">${escapeHtml(category?.description || '')}</textarea></label>
      <div class="form-actions"><button class="btn secondary" value="cancel" formnovalidate>Cancelar</button><button class="btn primary" value="save">${category ? 'Guardar cambios' : 'Crear categoría'}</button></div>
    </form>`;
    document.body.append(dialog);
    dialog.addEventListener('close', () => dialog.remove());
    dialog.addEventListener('click', (event) => { if (event.target === dialog) dialog.close('cancel'); });
    dialog.showModal();
    dialog.querySelector('form').addEventListener('submit', (event) => {
      event.preventDefault();
      const form = event.currentTarget;
      if (event.submitter?.value === 'cancel') { dialog.close('cancel'); return; }
      const name = form.elements.name.value.trim();
      if (!name) { form.elements.name.focus(); return; }
      const nameError = form.querySelector('#category-name-error');
      nameError.hidden = true;
      if (categories.some((entry) => entry.name.toLocaleLowerCase('es') === name.toLocaleLowerCase('es') && entry.id !== category?.id)) {
        nameError.textContent = 'Ya existe una categoría con ese nombre. Elige otro nombre.';
        nameError.hidden = false;
        form.elements.name.focus();
        return;
      }
      const nextCategory = { id: category?.id || makeId(), name, description: form.elements.description.value.trim() };
      const next = category ? categories.map((entry) => entry.id === category.id ? nextCategory : entry) : [...categories, nextCategory];
      if (write(CATEGORY_KEY, next)) {
        categories = next;
        dialog.close('save');
        renderCategories();
        refreshStats();
      }
    });
  }

  function renderCategories() {
    const grid = byId('category-grid');
    if (!grid) return;
    const term = byId('category-search').value.trim().toLocaleLowerCase('es');
    const matches = categories.filter((category) => `${category.name} ${category.description}`.toLocaleLowerCase('es').includes(term));
    byId('category-empty').hidden = matches.length > 0;
    grid.hidden = matches.length === 0;
    if (!categories.length) {
      byId('category-empty').querySelector('h2').textContent = 'Aún no hay categorías';
      byId('category-empty').querySelector('p').textContent = 'Crea una categoría para clasificar tus productos.';
      byId('empty-new-category').hidden = false;
    } else if (!matches.length) {
      byId('category-empty').querySelector('h2').textContent = 'No encontramos categorías';
      byId('category-empty').querySelector('p').textContent = 'Prueba con otro término de búsqueda.';
      byId('empty-new-category').hidden = true;
    }
    grid.innerHTML = matches.map((category) => {
      const count = products.filter((product) => product.categoryId === category.id).length;
      return `<article class="card category-card"><div class="cat-top"><span class="category-count">${count} ${count === 1 ? 'producto' : 'productos'}</span></div><h3>${escapeHtml(category.name)}</h3><p>${escapeHtml(category.description || 'Sin descripción.')}</p><div class="cat-bottom"><a class="btn secondary" href="/?categoria=${encodeURIComponent(category.id)}">Ver productos</a><div class="category-actions"><button class="btn subtle" data-edit-category="${escapeHtml(category.id)}" aria-label="Editar categoría ${escapeHtml(category.name)}">Editar</button><button class="btn danger" data-delete-category="${escapeHtml(category.id)}" aria-label="Eliminar categoría ${escapeHtml(category.name)}">Eliminar</button></div></div></article>`;
    }).join('');
    grid.querySelectorAll('[data-edit-category]').forEach((button) => button.addEventListener('click', () => {
      const category = categories.find((entry) => entry.id === button.dataset.editCategory);
      if (category) showCategoryDialog(category);
    }));
    grid.querySelectorAll('[data-delete-category]').forEach((button) => button.addEventListener('click', () => {
      const category = categories.find((entry) => entry.id === button.dataset.deleteCategory);
      if (!category) return;
      const used = products.some((product) => product.categoryId === category.id);
      if (used) { alert('No puedes eliminar una categoría que todavía tiene productos. Cambia primero esos productos a otra categoría.'); return; }
      if (confirm(`¿Eliminar la categoría “${category.name}”?`)) {
        const next = categories.filter((entry) => entry.id !== category.id);
        if (write(CATEGORY_KEY, next)) { categories = next; renderCategories(); refreshStats(); }
      }
    }));
  }

  function setupCategories() {
    if (!byId('category-grid')) return;
    byId('new-category').addEventListener('click', () => showCategoryDialog());
    byId('empty-new-category').addEventListener('click', () => showCategoryDialog());
    byId('category-search').addEventListener('input', renderCategories);
    byId('category-search-submit').addEventListener('click', renderCategories);
    let ascending = true;
    byId('sort-categories').addEventListener('click', () => {
      categories = [...categories].sort((a, b) => a.name.localeCompare(b.name, 'es') * (ascending ? 1 : -1));
      ascending = !ascending;
      byId('sort-categories').textContent = `Ordenar: ${ascending ? 'A–Z' : 'Z–A'}`;
      byId('sort-categories').setAttribute('aria-label', `Ordenar categorías de ${ascending ? 'A a Z' : 'Z a A'}`);
      write(CATEGORY_KEY, categories);
      renderCategories();
    });
    renderCategories();
  }

  const editMatch = path.match(/^\/productos\/(\d+)\/editar\/$/);
  const detailMatch = path.match(/^\/productos\/(\d+)\/$/);
  const deleteMatch = path.match(/^\/productos\/(\d+)\/eliminar\/$/);
  setupProductList();
  setupProductForm(editMatch ? decodeURIComponent(editMatch[1]) : null);
  if (detailMatch) setupDetail(decodeURIComponent(detailMatch[1]));
  if (deleteMatch) setupDelete(decodeURIComponent(deleteMatch[1]));
  setupCategories();
})();
