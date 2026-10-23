<template>
  <div class="site-shell">
    <header class="site-header"><RouterLink to="/" class="brand"><span class="brand-mark">Ф</span><span>ФОРМА<span class="brand-dot">.</span></span></RouterLink><nav><a href="#catalog">Каталог</a><a href="#about">О компании</a></nav><a class="header-contact" href="mailto:hello@forma.example">Обсудить проект <span>↗</span></a></header>
    <RouterView />
    <footer class="site-footer"><RouterLink to="/" class="brand"><span class="brand-mark">Ф</span><span>ФОРМА<span class="brand-dot">.</span></span></RouterLink><p>Технологии для тех, кто создаёт будущее.</p><a href="/api/docs" target="_blank">API docs ↗</a><span>© 2026 Форма</span></footer>
  </div>
</template>
