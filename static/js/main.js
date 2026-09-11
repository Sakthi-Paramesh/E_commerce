/* ================================================================
   ShopWave — main.js
   Global JavaScript utilities
================================================================ */

'use strict';

// ─── CSRF TOKEN HELPER ───────────────────────────────────────
function getCookie(name) {
  let v = null;
  if (document.cookie && document.cookie !== '') {
    document.cookie.split(';').forEach(c => {
      const t = c.trim();
      if (t.startsWith(name + '=')) v = decodeURIComponent(t.slice(name.length + 1));
    });
  }
  return v;
}

// ─── TOAST NOTIFICATION ──────────────────────────────────────
function showToast(type, message) {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const typeMap = { success: 'success', error: 'danger', warning: 'warning', info: 'info' };
  const iconMap = {
    success: 'bi-check-circle-fill',
    danger: 'bi-x-circle-fill',
    warning: 'bi-exclamation-triangle-fill',
    info: 'bi-info-circle-fill',
  };
  const cls = typeMap[type] || 'info';
  const icon = iconMap[cls] || 'bi-info-circle-fill';

  const div = document.createElement('div');
  div.className = `toast align-items-center text-bg-${cls} border-0`;
  div.setAttribute('role', 'alert');
  div.innerHTML = `
    <div class="d-flex">
      <div class="toast-body fw-500">
        <i class="bi ${icon} me-2"></i>${message}
      </div>
      <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
    </div>`;
  container.appendChild(div);

  const toast = new bootstrap.Toast(div, { delay: 4000 });
  toast.show();
  div.addEventListener('hidden.bs.toast', () => div.remove());
}

// ─── UPDATE NAV CART BADGE ───────────────────────────────────
function updateNavCartCount(count) {
  document.querySelectorAll('#navCartBadge, .cart-badge').forEach(el => {
    if (count > 0) {
      el.textContent = count;
      el.style.display = '';
    } else {
      el.style.display = 'none';
    }
  });
}

// ─── ADD TO CART ─────────────────────────────────────────────
function addToCart(productId, quantity = 1, btn = null) {
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Adding...';
  }

  fetch('/cart/add/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ product_id: productId, quantity: quantity }),
  })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        showToast('success', data.message);
        updateNavCartCount(data.cart_count);
        if (btn) {
          btn.innerHTML = '<i class="bi bi-check-lg me-1"></i>Added!';
          setTimeout(() => {
            btn.disabled = false;
            btn.innerHTML = '<i class="bi bi-cart-plus me-1"></i>Add to Cart';
          }, 2000);
        }
      } else {
        showToast('error', data.message || 'Could not add to cart.');
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = '<i class="bi bi-cart-plus me-1"></i>Add to Cart';
        }
      }
    })
    .catch(() => {
      showToast('error', 'Something went wrong. Please try again.');
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-cart-plus me-1"></i>Add to Cart';
      }
    });
}

// ─── BUY NOW ─────────────────────────────────────────────────
function buyNow(productId, btn = null) {
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Processing...';
  }

  fetch('/cart/buy-now/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ product_id: productId, quantity: 1 }),
  })
    .then(r => r.json())
    .then(data => {
      if (data.success) {
        window.location.href = data.redirect;
      } else {
        showToast('error', data.message || 'Could not process. Please try again.');
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = '<i class="bi bi-lightning-fill me-1"></i>Buy Now';
        }
      }
    })
    .catch(() => {
      showToast('error', 'Something went wrong. Please try again.');
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = '<i class="bi bi-lightning-fill me-1"></i>Buy Now';
      }
    });
}


// ─── TOGGLE WISHLIST ─────────────────────────────────────────
function toggleWishlist(productId, btn) {
  const icon = btn.querySelector('i');

  fetch('/wishlist/toggle/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ product_id: productId }),
  })
    .then(r => {
      if (r.status === 302 || r.redirected) {
        window.location.href = '/accounts/login/?next=' + window.location.pathname;
        return null;
      }
      return r.json();
    })
    .then(data => {
      if (!data) return;
      if (data.success) {
        showToast(data.added ? 'success' : 'info', data.message);

        // Update all wishlist buttons for this product
        document.querySelectorAll(`[onclick*="toggleWishlist(${productId}"]`).forEach(b => {
          const ic = b.querySelector('i');
          if (data.added) {
            b.classList.add('active');
            if (ic) ic.className = 'bi bi-heart-fill';
          } else {
            b.classList.remove('active');
            if (ic) ic.className = 'bi bi-heart';
          }
        });

        // Update product detail wishlist button text
        if (btn.id === 'wishlistBtn') {
          btn.innerHTML = data.added
            ? '<i class="bi bi-heart-fill me-2"></i>Wishlisted'
            : '<i class="bi bi-heart me-2"></i>Wishlist';
          btn.classList.toggle('active', data.added);
        }

        // Update wishlist count badge
        document.querySelectorAll('.wishlist-count-badge').forEach(el => {
          el.textContent = data.wishlist_count;
        });
      }
    })
    .catch(() => showToast('error', 'Could not update wishlist.'));
}

// ─── NAVBAR SCROLL EFFECT ────────────────────────────────────
window.addEventListener('scroll', () => {
  const nav = document.getElementById('mainNavbar');
  if (nav) {
    nav.classList.toggle('scrolled', window.scrollY > 30);
  }
});

// ─── SCROLL REVEAL ───────────────────────────────────────────
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      revealObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.1 });

document.addEventListener('DOMContentLoaded', () => {
  // Apply reveal to sections
  document.querySelectorAll('.sw-section, .feature-card, .testimonial-card, .category-card, .product-card').forEach(el => {
    el.classList.add('reveal');
    revealObserver.observe(el);
  });

  // Auto-show Django message toasts
  document.querySelectorAll('.toast.show').forEach(el => {
    const t = new bootstrap.Toast(el, { delay: 4000 });
    t.show();
  });
});

// ─── SMOOTH SCROLL for anchor links ─────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
