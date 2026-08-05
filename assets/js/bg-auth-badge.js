/*
 * bg-auth-badge.js — indicador de sesion/suscripcion en la cabecera.
 *
 * Rellena dos placeholders:
 *   - <li id="bg-profile-status"></li> (a la izquierda de Dashboard): icono de perfil +
 *     username, solo para suscriptor logado.
 *   - <li id="bg-auth-status"></li> (tras Pricing): pill "Log in" para anonimos.
 * Tambien oculta el icono estatico de Login (<li id="bg-login-icon">, solo existe en la
 * plantilla raiz) cuando ya no hace falta.
 *
 * Nace porque hay suscriptores que ven las graficas recortadas (AVIV, M2...) sin darse
 * cuenta de que simplemente no han iniciado sesion en ese navegador.
 *
 * Fuentes de verdad, ambas cookies de dominio padre `.bgeometrics.com` emitidas por BGUser:
 *   - bgIsSubscriber() (bg-chart-data.js), lee `bg_full=1`: suscriptor de pago activo.
 *     Se reutiliza tal cual para que el badge y la banda naranja de las graficas
 *     (chart-upgrade-band.js) nunca puedan discrepar.
 *   - cookie `bg_user` (username URL-encoded): se emite en TODO login exitoso, sea cual sea
 *     el tier. Es la unica forma de detectar "logado" en JS, porque `bg_token` es HttpOnly.
 *
 * Estados:
 *   - Suscriptor (bg_full=1): oculta el icono de Login; a la izquierda de Dashboard aparece
 *     un icono de perfil + el username, enlazando a /profile.
 *   - Logado pero no suscriptor (bg_user si, bg_full no): sin badge de ningun tipo (no se le
 *     ofrece login, ya esta logado) — el icono de Login sigue visible por si quiere cambiar
 *     de cuenta.
 *   - Anonimo (ninguna cookie): solo el pill ambar "Log in"; el icono de Login se oculta
 *     porque seria redundante (el propio pill ya lleva a /login).
 */

(function () {

    var PORTAL = 'https://portal.bgeometrics.com';

    // color:#000000 explicito (no `inherit`): en el tema dark el color heredado es gris
    // claro y el texto quedaria ilegible sobre el fondo del badge.
    var PILL = 'display:inline-flex;align-items:center;gap:5px;' +
               'padding:4px 10px;border-radius:12px;font-size:12px;font-weight:bold;' +
               'color:#000000;text-decoration:none;white-space:nowrap;' +
               'box-shadow:0 1px 3px rgba(0,0,0,0.4);';

    var MAX_USERNAME_CHARS = 16;

    function getCookie(name) {
        var re = new RegExp('(?:^|; )' + name.replace(/([.$?*|{}()\[\]\\/+^])/g, '\\$1') + '=([^;]*)');
        var m = document.cookie.match(re);
        if (!m || !m[1]) return null;
        try {
            return decodeURIComponent(m[1]);
        } catch (e) {
            return null;
        }
    }

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    function displayName(username) {
        var safe = escapeHtml(username);
        if (safe.length > MAX_USERNAME_CHARS) {
            return safe.slice(0, MAX_USERNAME_CHARS - 1) + '…';
        }
        return safe;
    }

    function setLoginIconVisible(visible) {
        var loginIcon = document.getElementById('bg-login-icon');
        if (loginIcon) {
            loginIcon.style.display = visible ? '' : 'none';
        }
    }

    function render() {
        var authHost = document.getElementById('bg-auth-status');
        var profileHost = document.getElementById('bg-profile-status');
        if (!authHost && !profileHost) {
            return; // pagina sin cabecera (p.ej. un grafico embebido) → no hace nada
        }

        var isSub = (typeof bgIsSubscriber === 'function') && bgIsSubscriber();
        var username = getCookie('bg_user');
        var isLoggedIn = !!username;
        var isEs = (document.documentElement.lang || '').toLowerCase().indexOf('es') === 0;

        if (isSub) {
            setLoginIconVisible(false);
            if (authHost) authHost.innerHTML = '';
            if (profileHost) {
                // Fallback a "Subscriber"/"Suscriptor": sesiones emitidas antes de este
                // cambio tienen bg_full pero todavia no tienen bg_user.
                profileHost.innerHTML =
                    '<a href="' + PORTAL + '/profile" style="' + PILL +
                        'background:#10b981;margin-right:10px;" title="' +
                        (isEs ? 'Sesion iniciada — historico completo desbloqueado'
                              : 'Signed in — full history unlocked') + '">' +
                      '<i class="bi bi-person-circle"></i>' +
                      '<span class="d-none d-md-inline">' +
                        (username ? displayName(username) : (isEs ? 'Suscriptor' : 'Subscriber')) +
                      '</span>' +
                    '</a>';
            }
            return;
        }

        if (profileHost) profileHost.innerHTML = '';

        if (isLoggedIn) {
            // Logado pero sin acceso completo (FREE): ya se le ha ofrecido iniciar sesion,
            // asi que no tiene sentido seguir mostrando el aviso de "Log in". El icono de
            // Login se deja visible por si quiere cambiar de cuenta.
            setLoginIconVisible(true);
            if (authHost) authHost.innerHTML = '';
            return;
        }

        // Anonimo: el propio pill "Log in" ya lleva a /login, asi que el icono de Login
        // por separado sobra.
        setLoginIconVisible(false);
        if (authHost) {
            authHost.innerHTML =
                '<a href="' + PORTAL + '/login" style="' + PILL + 'background:#F7931A;margin-right:10px;" title="' +
                    (isEs ? 'Historico limitado. Inicia sesion con tu suscripcion para verlo completo'
                          : 'Limited history. Log in with your subscription to see it in full') + '">' +
                  '<i class="bi bi-lock-fill"></i>' +
                  '<span class="d-none d-md-inline">' +
                    (isEs ? 'Iniciar sesion' : 'Log in') +
                  '</span>' +
                '</a>';
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', render);
    } else {
        render();
    }

})();
