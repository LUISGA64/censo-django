// PWA Manager - Progressive Web App
class PWAManager {
  constructor() {
    this.swRegistration = null;
    this.deferredPrompt = null;
    this.isOnline = navigator.onLine;
    this.init();
  }

  init() {
    if ('serviceWorker' in navigator) {
      this.registerServiceWorker();
    }
    this.setupInstallPrompt();
    this.setupOnlineOfflineHandlers();
  }

  async registerServiceWorker() {
    try {
      const registration = await navigator.serviceWorker.register('/static/sw.js');
      this.swRegistration = registration;
      console.log('✅ Service Worker registrado');

      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing;
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            this.showUpdateNotification();
          }
        });
      });
    } catch (error) {
      console.error('❌ Error SW:', error);
    }
  }

  setupInstallPrompt() {
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      this.deferredPrompt = e;
      this.showInstallButton();
    });
  }

  showInstallButton() {
    const btn = document.getElementById('pwa-install-btn');
    if (btn) {
      btn.style.display = 'block';
      btn.onclick = () => this.promptInstall();
    }
  }

  async promptInstall() {
    if (!this.deferredPrompt) return;
    this.deferredPrompt.prompt();
    const { outcome } = await this.deferredPrompt.userChoice;
    console.log(`Instalación ${outcome}`);
    this.deferredPrompt = null;
  }

  setupOnlineOfflineHandlers() {
    window.addEventListener('online', () => {
      this.isOnline = true;
      console.log('🟢 Online');
      if (typeof Swal !== 'undefined') {
        Swal.fire({
          icon: 'success',
          title: 'Conexión Restaurada',
          timer: 2000,
          toast: true,
          position: 'top-end',
          showConfirmButton: false
        });
      }
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
      console.log('🔴 Offline');
      if (typeof Swal !== 'undefined') {
        Swal.fire({
          icon: 'warning',
          title: 'Sin Conexión',
          text: 'Modo offline activo',
          timer: 3000,
          toast: true,
          position: 'top-end',
          showConfirmButton: false
        });
      }
    });
  }

  showUpdateNotification() {
    if (typeof Swal !== 'undefined') {
      Swal.fire({
        title: 'Actualización Disponible',
        text: 'Nueva versión de la app',
        icon: 'info',
        showCancelButton: true,
        confirmButtonText: 'Actualizar',
        confirmButtonColor: '#2196F3'
      }).then((result) => {
        if (result.isConfirmed && this.swRegistration.waiting) {
          this.swRegistration.waiting.postMessage({ action: 'skipWaiting' });
          window.location.reload();
        }
      });
    }
  }
}

// Inicializar
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.pwaManager = new PWAManager();
  });
} else {
  window.pwaManager = new PWAManager();
}
