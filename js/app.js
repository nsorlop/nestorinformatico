/* ==========================================================================
   Informática Néstor
   JavaScript de la web.

   Reglas que se cumplen aquí y que se prometen en la política de privacidad:
   - No se carga nada de ningún servidor ajeno.
   - No se envía ningún dato a ninguna parte. El formulario sólo prepara el
     texto y abre WhatsApp o el programa de correo del propio visitante.
   - Lo único que se guarda en el navegador es si ya se ha cerrado el aviso
     de idioma.
   - La web funciona entera sin JavaScript. Esto sólo añade comodidades.
   ========================================================================== */
(function () {
  'use strict';

  var TEL_WA = '34644219118';
  var CORREO = 'nestorlafont@gmail.com';

  function leer(clave) {
    try { return window.localStorage.getItem(clave); } catch (e) { return null; }
  }
  function guardar(clave, valor) {
    try { window.localStorage.setItem(clave, valor); } catch (e) { /* modo privado */ }
  }

  /* ----------------------------------------------------------------------
     1. Aviso de idioma
        Si el navegador está en valenciano o catalán y se está viendo la
        versión en castellano (o al revés), se ofrece la otra. Una sola vez.
     ---------------------------------------------------------------------- */
  function iniciarAvisoIdioma() {
    var aviso = document.getElementById('aviso-idioma');
    if (!aviso || leer('aviso-idioma') === 'cerrado') { return; }

    var idiomaPagina = document.documentElement.lang || 'es';
    var idiomas = (navigator.languages || [navigator.language || '']).join(',').toLowerCase();
    var quiereValenciano = /(^|,)\s*(ca|val)\b/.test(idiomas);
    var enValenciano = idiomaPagina.toLowerCase().indexOf('ca') === 0;

    if (enValenciano ? quiereValenciano : !quiereValenciano) { return; }

    aviso.hidden = false;
    var cerrar = aviso.querySelector('[data-cerrar-aviso]');
    if (cerrar) {
      cerrar.addEventListener('click', function () {
        aviso.hidden = true;
        guardar('aviso-idioma', 'cerrado');
      });
    }
  }

  /* ----------------------------------------------------------------------
     2. Formulario: no envía nada, sólo prepara el mensaje
     ---------------------------------------------------------------------- */
  function valor(id) {
    var el = document.getElementById(id);
    return el ? el.value.trim() : '';
  }

  function construirMensaje() {
    var f = document.getElementById('formulario');
    if (!f) { return ''; }
    var plantilla = f.getAttribute('data-plantilla') ||
      'Hola, soy {nombre} de {pueblo}. Mi teléfono es {telefono}. {problema}';
    return plantilla
      .replace('{nombre}', valor('f-nombre') || '...')
      .replace('{pueblo}', valor('f-pueblo') || '...')
      .replace('{telefono}', valor('f-telefono') || '...')
      .replace('{problema}', valor('f-problema') || '...');
  }

  function faltaAlgo() {
    var error = document.getElementById('form-error');
    var obligatorios = ['f-nombre', 'f-telefono', 'f-problema'];
    for (var i = 0; i < obligatorios.length; i++) {
      var el = document.getElementById(obligatorios[i]);
      if (el && !el.value.trim()) {
        if (error) { error.hidden = false; }
        el.focus();
        return true;
      }
    }
    if (error) { error.hidden = true; }
    return false;
  }

  function iniciarFormulario() {
    var f = document.getElementById('formulario');
    if (!f) { return; }

    f.addEventListener('submit', function (ev) { ev.preventDefault(); });

    var porWhatsapp = document.getElementById('enviar-whatsapp');
    if (porWhatsapp) {
      porWhatsapp.addEventListener('click', function () {
        if (faltaAlgo()) { return; }
        window.open('https://wa.me/' + TEL_WA + '?text=' +
                    encodeURIComponent(construirMensaje()), '_blank', 'noopener');
      });
    }

    var porCorreo = document.getElementById('enviar-correo');
    if (porCorreo) {
      porCorreo.addEventListener('click', function () {
        if (faltaAlgo()) { return; }
        window.location.href = 'mailto:' + CORREO +
          '?subject=' + encodeURIComponent(f.getAttribute('data-asunto') || 'Consulta') +
          '&body=' + encodeURIComponent(construirMensaje());
      });
    }
  }

  /* ----------------------------------------------------------------------
     3. Año del pie y apertura de la pregunta enlazada
     ---------------------------------------------------------------------- */
  function iniciarAnyo() {
    var el = document.getElementById('anyo');
    if (el) { el.textContent = String(new Date().getFullYear()); }
  }

  function abrirDestino() {
    if (!window.location.hash) { return; }
    var destino;
    try { destino = document.querySelector(window.location.hash); } catch (e) { return; }
    if (destino && destino.tagName === 'DETAILS') { destino.open = true; }
  }

  function arrancar() {
    iniciarAvisoIdioma();
    iniciarFormulario();
    iniciarAnyo();
    abrirDestino();
    window.addEventListener('hashchange', abrirDestino);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', arrancar);
  } else {
    arrancar();
  }
})();
