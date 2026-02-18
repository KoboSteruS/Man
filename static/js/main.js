/**
 * Лендинг «Московское Агентство Недвижимости»
 * Поведение: хедер при скролле, мобильное меню, форма, тост
 */
(function () {
  'use strict';

  var HEADER_SCROLL_THRESHOLD = 50;

  // ---------- Header scroll (throttled) ----------
  var header = document.getElementById('header');
  if (header) {
    var scrollScheduled = false;
    function updateHeader() {
      header.classList.toggle('is-scrolled', window.scrollY > HEADER_SCROLL_THRESHOLD);
      scrollScheduled = false;
    }
    function onScroll() {
      if (!scrollScheduled) {
        scrollScheduled = true;
        requestAnimationFrame(updateHeader);
      }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    updateHeader();
  }

  // ---------- Mobile menu (burger) ----------
  var burger = document.getElementById('header-burger');
  var mobileMenu = document.getElementById('header-mobile-menu');
  if (burger && mobileMenu) {
    function openMenu() {
      header.classList.add('is-open');
      burger.setAttribute('aria-expanded', 'true');
      mobileMenu.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }
    function closeMenu() {
      header.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
      mobileMenu.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }
    burger.addEventListener('click', function () {
      if (header.classList.contains('is-open')) {
        closeMenu();
      } else {
        openMenu();
      }
    });
    mobileMenu.querySelectorAll('.header__mobile-link, .header__mobile-phone, .header__mobile-cta').forEach(function (link) {
      link.addEventListener('click', closeMenu);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && header.classList.contains('is-open')) {
        closeMenu();
      }
    });
  }

  // ---------- Contact form & toast ----------
  var contactForm = document.getElementById('contact-form');
  var toast = document.getElementById('toast');
  var toastMessage = toast ? toast.querySelector('.toast__message') : null;

  function showToast(message, type) {
    type = type || 'success';
    if (!toast || !toastMessage) return;
    toast.className = 'toast toast--' + type + ' is-visible';
    toastMessage.textContent = message;
    toast.hidden = false;
    setTimeout(function () {
      toast.classList.remove('is-visible');
      setTimeout(function () {
        toast.hidden = true;
      }, 300);
    }, 4000);
  }

  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var nameEl = contactForm.querySelector('#name');
      var phoneEl = contactForm.querySelector('#phone');
      var emailEl = contactForm.querySelector('#email');
      var messageEl = contactForm.querySelector('#message');
      if (nameEl && !nameEl.value.trim()) {
        nameEl.focus();
        showToast('Укажите имя', 'error');
        return;
      }
      if (phoneEl && !phoneEl.value.trim()) {
        phoneEl.focus();
        showToast('Укажите телефон', 'error');
        return;
      }
      var submitBtn = contactForm.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.setAttribute('aria-busy', 'true');
      }
      fetch('/api/send-lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: nameEl ? nameEl.value.trim() : '',
          phone: phoneEl ? phoneEl.value.trim() : '',
          email: emailEl ? emailEl.value.trim() : '',
          message: messageEl ? messageEl.value.trim() : ''
        })
      })
        .then(function (r) { return r.json().then(function (data) { return { ok: r.ok, data: data }; }); })
        .then(function (res) {
          if (res.ok && res.data.ok) {
            showToast('Спасибо! Мы свяжемся с вами в ближайшее время.', 'success');
            contactForm.reset();
          } else {
            showToast(res.data.error || 'Не удалось отправить заявку. Попробуйте позже.', 'error');
          }
        })
        .catch(function () {
          showToast('Ошибка сети. Попробуйте позже.', 'error');
        })
        .finally(function () {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.removeAttribute('aria-busy');
          }
        });
    });
  }

  // ---------- Fallback для фото: если локальный файл не найден (404), подставить data-fallback ----------
  document.querySelectorAll('img[data-fallback]').forEach(function (img) {
    img.addEventListener('error', function () {
      var fallback = this.getAttribute('data-fallback');
      if (fallback) {
        this.removeAttribute('data-fallback');
        this.src = fallback;
      }
    });
  });

  // ---------- Лайтбокс сертификатов руководителя ----------
  var certLightbox = document.getElementById('cert-lightbox');
  var certLightboxImg = document.getElementById('cert-lightbox-img');
  var certLightboxClose = document.getElementById('cert-lightbox-close');
  var certLightboxBackdrop = document.getElementById('cert-lightbox-backdrop');
  if (certLightbox && certLightboxImg) {
    function openCertLightbox(src) {
      certLightboxImg.src = src;
      certLightbox.hidden = false;
      document.body.style.overflow = 'hidden';
    }
    function closeCertLightbox() {
      certLightbox.hidden = true;
      document.body.style.overflow = '';
    }
    document.querySelectorAll('.leader-cert').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var full = this.getAttribute('data-full');
        if (full) openCertLightbox(full);
      });
    });
    if (certLightboxClose) certLightboxClose.addEventListener('click', closeCertLightbox);
    if (certLightboxBackdrop) certLightboxBackdrop.addEventListener('click', closeCertLightbox);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && certLightbox && !certLightbox.hidden) closeCertLightbox();
    });
  }

  // ---------- Модальное окно «Все новости» (сортировка по дате создания) ----------
  var allNewsModal = document.getElementById('all-news-modal');
  var allNewsModalList = document.getElementById('all-news-modal-list');
  var allNewsModalClose = document.getElementById('all-news-modal-close');
  var allNewsModalBackdrop = document.getElementById('all-news-modal-backdrop');
  var openAllNewsBtn = document.getElementById('open-all-news-modal');
  if (allNewsModal && allNewsModalList) {
    function openAllNewsModal() {
      var cards = document.querySelectorAll('.news-card[data-news-sort][data-news-body-id]');
      var items = [];
      cards.forEach(function (card) {
        var bodyId = card.getAttribute('data-news-body-id');
        var body = '';
        if (bodyId) {
          var bodyEl = document.getElementById(bodyId);
          if (bodyEl) body = bodyEl.textContent.trim();
        }
        items.push({
          title: card.getAttribute('data-news-title') || '',
          date: card.getAttribute('data-news-date') || '',
          sort: card.getAttribute('data-news-sort') || '0000-00-00',
          body: body,
          image: card.getAttribute('data-news-image') || ''
        });
      });
      items.sort(function (a, b) { return b.sort.localeCompare(a.sort); });
      allNewsModalList.innerHTML = '';
      items.forEach(function (item) {
        var article = document.createElement('article');
        article.className = 'all-news-modal__item';
        article.innerHTML =
          '<p class="all-news-modal__date">' + escapeHtml(item.date) + '</p>' +
          '<h3 class="all-news-modal__item-title">' + escapeHtml(item.title) + '</h3>' +
          '<div class="all-news-modal__item-body">' + escapeHtml(item.body) + '</div>';
        allNewsModalList.appendChild(article);
      });
      allNewsModal.hidden = false;
      document.body.style.overflow = 'hidden';
      if (allNewsModalClose) allNewsModalClose.focus();
    }
    function closeAllNewsModal() {
      allNewsModal.hidden = true;
      document.body.style.overflow = '';
    }
    function escapeHtml(text) {
      var div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }
    if (openAllNewsBtn) openAllNewsBtn.addEventListener('click', openAllNewsModal);
    if (allNewsModalClose) allNewsModalClose.addEventListener('click', closeAllNewsModal);
    if (allNewsModalBackdrop) allNewsModalBackdrop.addEventListener('click', closeAllNewsModal);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && allNewsModal && !allNewsModal.hidden) closeAllNewsModal();
    });
  }

  // ---------- Модальное окно проектов (по клику на карточку услуги) ----------
  var projectsModal = document.getElementById('projects-modal');
  var projectsModalTitle = document.getElementById('projects-modal-title');
  var projectsModalLead = document.getElementById('projects-modal-lead');
  var projectsModalBeforeAfter = document.getElementById('projects-modal-before-after');
  var projectsModalClose = document.getElementById('projects-modal-close');
  var projectsModalBackdrop = document.getElementById('projects-modal-backdrop');
  var closeProjectsModal = function () {};
  if (projectsModal && projectsModalTitle && projectsModalLead) {
    function openProjectsModal(title, lead, modalId) {
      projectsModalTitle.textContent = title || '';
      projectsModalLead.textContent = lead || '';
      if (projectsModalBeforeAfter) {
        if (modalId === 'gallery2') {
          projectsModalBeforeAfter.hidden = false;
        } else {
          projectsModalBeforeAfter.hidden = true;
        }
      }
      projectsModal.hidden = false;
      document.body.style.overflow = 'hidden';
      projectsModalClose.focus();
    }
    closeProjectsModal = function () {
      projectsModal.hidden = true;
      document.body.style.overflow = '';
      if (projectDetailModal && !projectDetailModal.hidden) {
        projectDetailModal.hidden = true;
        if (projectDetailBody) projectDetailBody.innerHTML = '';
      }
    };
    document.querySelectorAll('[data-open-projects-modal]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var title = this.getAttribute('data-modal-title');
        var lead = this.getAttribute('data-modal-lead');
        var modalId = this.getAttribute('data-modal-id');
        openProjectsModal(title, lead, modalId);
      });
    });
    if (projectsModalClose) projectsModalClose.addEventListener('click', closeProjectsModal);
    if (projectsModalBackdrop) projectsModalBackdrop.addEventListener('click', closeProjectsModal);
  }

  // ---------- Переключатель До/После (вызывать для контейнера) ----------
  function bindRemontToggles(container) {
    if (!container) return;
    container.querySelectorAll('[data-remont-toggle]').forEach(function (figure) {
      var wrap = figure.querySelector('.remont-item__switch-wrap');
      var btns = figure.querySelectorAll('.remont-item__switch-btn');
      if (!wrap || !btns.length) return;
      btns.forEach(function (btn) {
        btn.addEventListener('click', function () {
          var show = this.getAttribute('data-show');
          btns.forEach(function (b) { b.classList.remove('is-active'); });
          this.classList.add('is-active');
          if (show === 'after') {
            wrap.classList.add('is-after');
          } else {
            wrap.classList.remove('is-after');
          }
        });
      });
    });
  }
  bindRemontToggles(document);

  // ---------- Модалка детали проекта (по клику на карточку проекта) ----------
  var projectDetailModal = document.getElementById('project-detail-modal');
  var projectDetailTitle = document.getElementById('project-detail-title');
  var projectDetailBody = document.getElementById('project-detail-body');
  var projectDetailClose = document.getElementById('project-detail-close');
  var projectDetailBackdrop = document.getElementById('project-detail-backdrop');
  document.querySelectorAll('[data-open-project-detail]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = this.getAttribute('data-project-id');
      var caption = this.querySelector('.remont-card__caption');
      var titleText = caption ? caption.textContent.trim() : 'Проект';
      var source = document.getElementById('project-content-' + id);
      if (!projectDetailModal || !projectDetailBody) return;
      if (source) {
        projectDetailBody.innerHTML = source.innerHTML;
        bindRemontToggles(projectDetailBody);
      } else {
        projectDetailBody.innerHTML = '';
      }
      if (projectDetailTitle) projectDetailTitle.textContent = titleText;
      projectDetailModal.hidden = false;
      document.body.style.overflow = 'hidden';
      if (projectDetailClose) projectDetailClose.focus();
    });
  });
  function closeProjectDetailModal() {
    if (projectDetailModal) {
      projectDetailModal.hidden = true;
      if (projectDetailBody) projectDetailBody.innerHTML = '';
      // overflow не сбрасываем — под ней может быть открыта модалка списка проектов
    }
  }
  if (projectDetailClose) projectDetailClose.addEventListener('click', closeProjectDetailModal);
  if (projectDetailBackdrop) projectDetailBackdrop.addEventListener('click', closeProjectDetailModal);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (projectDetailModal && !projectDetailModal.hidden) {
        closeProjectDetailModal();
      } else if (projectsModal && !projectsModal.hidden) {
        closeProjectsModal();
      }
    }
  });

})();
