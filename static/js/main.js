/**
 * main.js — JavaScript global
 * ---------------------------------------------------------------------------
 * Se carga en todas las páginas desde base.html.
 * Contenido:
 *   1. Utilidades compartidas (window.Blog)
 *   2. Mensajes flash (toast): cierre manual y automático
 *   3. Dropdown del menú de usuario
 */
(function () {
    'use strict';

    /* ======================================================================
       1. UTILIDADES COMPARTIDAS
       Otros scripts (ej. users.js) pueden usar window.Blog.getCookie, etc.
       ====================================================================== */

    /**
     * Lee una cookie por nombre. Se usa para obtener el token CSRF
     * en peticiones fetch (POST) hacia Django.
     * @param {string} name - Nombre de la cookie (ej. 'csrftoken').
     * @returns {string|null} Valor de la cookie o null si no existe.
     */
    function getCookie(name) {
        const match = document.cookie
            .split('; ')
            .find((row) => row.startsWith(name + '='));
        return match ? decodeURIComponent(match.split('=')[1]) : null;
    }

    window.Blog = { getCookie: getCookie };


    /* ======================================================================
       2. MENSAJES FLASH (TOAST)
       ====================================================================== */

    const TOAST_AUTO_HIDE_MS = 5000; // Tiempo antes de ocultarse solo
    const TOAST_ANIMATION_MS = 300;  // Debe coincidir con la transición CSS

    /**
     * Oculta un toast con animación y lo elimina del DOM.
     * @param {HTMLElement} toast - Elemento .toast a cerrar.
     */
    function dismissToast(toast) {
        toast.classList.add('is-hiding');
        setTimeout(() => toast.remove(), TOAST_ANIMATION_MS);
    }

    function initToasts() {
        document.querySelectorAll('.toast').forEach((toast) => {
            // Cierre automático
            setTimeout(() => dismissToast(toast), TOAST_AUTO_HIDE_MS);

            // Cierre manual con el botón ×
            const closeBtn = toast.querySelector('[data-dismiss-toast]');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => dismissToast(toast));
            }
        });
    }


    /* ======================================================================
       3. DROPDOWN DEL MENÚ DE USUARIO
       Estructura esperada (ver partials/navbar.html):
         [data-dropdown] > [data-dropdown-toggle] + .dropdown__menu[hidden]
       ====================================================================== */

    function initDropdowns() {
        const dropdowns = document.querySelectorAll('[data-dropdown]');

        dropdowns.forEach((dropdown) => {
            const toggle = dropdown.querySelector('[data-dropdown-toggle]');
            const menu = dropdown.querySelector('.dropdown__menu');
            if (!toggle || !menu) return;

            // Abrir / cerrar al hacer clic en el botón
            toggle.addEventListener('click', (event) => {
                event.stopPropagation();
                menu.hidden = !menu.hidden;
            });
        });

        // Cerrar al hacer clic fuera
        document.addEventListener('click', () => {
            dropdowns.forEach((d) => {
                const menu = d.querySelector('.dropdown__menu');
                if (menu) menu.hidden = true;
            });
        });

        // Cerrar con la tecla Escape
        document.addEventListener('keydown', (event) => {
            if (event.key !== 'Escape') return;
            dropdowns.forEach((d) => {
                const menu = d.querySelector('.dropdown__menu');
                if (menu) menu.hidden = true;
            });
        });
    }


        /* ======================================================================
       4. BOTÓN SEGUIR / SIGUIENDO (perfil)
       Estructura esperada (ver user/profile.html):
         button[data-follow-btn][data-url][data-following="true|false"]
       La vista UserFollowView responde { success, following }.
       ====================================================================== */

    function initFollowButtons() {
        document.querySelectorAll('[data-follow-btn]').forEach((btn) => {
            btn.addEventListener('click', async () => {
                btn.disabled = true; // Evita dobles clics mientras responde
                try {
                    const response = await fetch(btn.dataset.url, {
                        method: 'POST',
                        headers: { 'X-CSRFToken': getCookie('csrftoken') },
                    });
                    const data = await response.json();
                    if (!data.success) return;

                    // Actualizar aspecto del botón
                    btn.dataset.following = String(data.following);
                    btn.textContent = data.following ? 'Siguiendo' : 'Seguir';
                    btn.classList.toggle('btn--primary', !data.following);
                    btn.classList.toggle('btn--secondary', data.following);

                    // Ajustar el contador de seguidores en ±1
                    const counter = document.querySelector('[data-followers-count]');
                    if (counter) {
                        counter.textContent = parseInt(counter.textContent, 10) + (data.following ? 1 : -1);
                    }
                } catch (error) {
                    console.error('No se pudo actualizar el seguimiento:', error);
                } finally {
                    btn.disabled = false;
                }
            });
        });
    }


    /* ======================================================================
       5. VISTA PREVIA DEL AVATAR (editar perfil)
       Estructura esperada (ver user/update_profile.html):
         input[data-avatar-input] y .avatar[data-avatar-preview]
       ====================================================================== */

    function initAvatarPreview() {
        const input = document.querySelector('[data-avatar-input]');
        const preview = document.querySelector('[data-avatar-preview]');
        if (!input || !preview) return;

        input.addEventListener('change', () => {
            const file = input.files[0];
            if (!file) return;

            // Sustituye el contenido del círculo por la imagen elegida
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            img.alt = 'Vista previa del avatar';
            preview.replaceChildren(img);
        });
    }


        /* ======================================================================
       6. ME GUSTA (publicaciones y comentarios)
       Estructura esperada: button[data-like-btn][data-url] dentro de un
       <article> que contenga un [data-like-count] con el total.
       Las vistas PostLikeView / CommentLikeView responden { liked, total_likes }.
       ====================================================================== */

    function initLikeButtons() {
        document.querySelectorAll('[data-like-btn]').forEach((btn) => {
            btn.addEventListener('click', async () => {
                btn.disabled = true; // Evita dobles clics mientras responde
                try {
                    const response = await fetch(btn.dataset.url, {
                        method: 'POST',
                        headers: { 'X-CSRFToken': getCookie('csrftoken') },
                    });
                    const data = await response.json();
                    if (!data.success) return;

                    // Actualizar contador (el más cercano dentro del mismo artículo)
                    const scope = btn.closest('article') || document;
                    const counter = scope.querySelector('[data-like-count]');
                    if (counter) counter.textContent = data.total_likes;

                    // Marcar / desmarcar visualmente
                    btn.classList.toggle('is-liked', data.liked);
                } catch (error) {
                    console.error('No se pudo registrar el me gusta:', error);
                } finally {
                    btn.disabled = false;
                }
            });
        });
    }


    /* ======================================================================
       7. FORMULARIO DE RESPUESTA A COMENTARIOS
       Estructura esperada: button[data-reply-toggle="<id del form>"]
       ====================================================================== */

    function initReplyToggles() {
        document.querySelectorAll('[data-reply-toggle]').forEach((btn) => {
            btn.addEventListener('click', () => {
                const form = document.getElementById(btn.dataset.replyToggle);
                if (!form) return;
                form.hidden = !form.hidden;
                if (!form.hidden) form.querySelector('textarea').focus();
            });
        });
    }


    /* ======================================================================
       INICIALIZACIÓN
       ====================================================================== */
    document.addEventListener('DOMContentLoaded', () => {
        initToasts();
        initDropdowns();
        initFollowButtons();
        initAvatarPreview();
        initLikeButtons();
        initReplyToggles();
    });
})();