<template>
  <div class="site-shell">
    <header class="site-header"><RouterLink to="/" class="brand"><span class="brand-mark">Э</span><span>EDUTECH<span class="brand-dot">.</span></span></RouterLink><nav><RouterLink to="/">Каталог</RouterLink><a href="/#about">О проекте</a></nav><RouterLink to="/admin" class="header-contact">Админ-панель <span>↗</span></RouterLink></header>
    <RouterView />
    <footer class="site-footer"><RouterLink to="/" class="brand"><span class="brand-mark">Э</span><span>EDUTECH<span class="brand-dot">.</span></span></RouterLink><p>Учебное оборудование для технического творчества.</p><a href="/api/docs" target="_blank">API docs ↗</a><span>© 2026 EduTech</span></footer>
  </div>
</template>
