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

})();
