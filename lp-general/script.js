// トータルHipサポーター LP1
// 1) FAQ開閉  2) 追従CTAの表示制御  3) CTAクリック計測フック（GA4はダミー）
(function () {
  'use strict';

  // FAQアコーディオン
  document.querySelectorAll('.faq-item dt').forEach(function (dt) {
    dt.setAttribute('role', 'button');
    dt.setAttribute('tabindex', '0');
    var toggle = function () { dt.parentElement.classList.toggle('open'); };
    dt.addEventListener('click', toggle);
    dt.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
    });
  });

  // 追従CTA: FVを過ぎたら表示・最終CTA付近では隠す
  var sticky = document.getElementById('stickyCta');
  var fv = document.querySelector('.fv');
  var finalCta = document.querySelector('.final-cta') || document.querySelector('.order');
  if (sticky && fv && finalCta && 'IntersectionObserver' in window) {
    var fvVisible = true, finalVisible = false;
    var update = function () {
      var show = !fvVisible && !finalVisible;
      sticky.classList.toggle('visible', show);
      sticky.setAttribute('aria-hidden', String(!show));
    };
    new IntersectionObserver(function (entries) {
      fvVisible = entries[0].isIntersecting; update();
    }, { threshold: 0.1 }).observe(fv);
    new IntersectionObserver(function (entries) {
      finalVisible = entries[0].isIntersecting; update();
    }, { threshold: 0.1 }).observe(finalCta || fv);
  }

  // CTAクリック計測（GA4タグ導入後に有効化される）
  document.querySelectorAll('.js-cta').forEach(function (a) {
    a.addEventListener('click', function () {
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'cta_click', {
          link_url: a.href,
          page_type: 'lp_general'
        });
      }
    });
  });
})();
