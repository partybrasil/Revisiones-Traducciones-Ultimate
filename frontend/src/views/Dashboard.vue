<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-2xl font-bold text-gray-900">
              Revisiones-Traducciones-Ultimate
            </h1>
            <p class="text-sm text-gray-500 mt-1">
              Sistema de Gestión de Fichas de Producto Multiidioma
            </p>
          </div>
          <div class="flex items-center space-x-4">
            <span class="badge badge-success">v1.0.0</span>
            <span class="badge badge-info">{{ status }}</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="card animate-fade-in">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500">Productos</p>
              <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.products }}</p>
            </div>
            <div class="bg-primary-light rounded-full p-3">
              <svg class="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
            </div>
          </div>
        </div>

        <div class="card animate-fade-in" style="animation-delay: 0.1s">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500">Familias</p>
              <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.families }}</p>
            </div>
            <div class="bg-green-100 rounded-full p-3">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
          </div>
        </div>

        <div class="card animate-fade-in" style="animation-delay: 0.2s">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500">Idiomas</p>
              <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.languages }}</p>
            </div>
            <div class="bg-yellow-100 rounded-full p-3">
              <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129" />
              </svg>
            </div>
          </div>
        </div>

        <div class="card animate-fade-in" style="animation-delay: 0.3s">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm text-gray-500">Compliance</p>
              <p class="text-2xl font-bold text-gray-900 mt-1">{{ stats.compliance }}%</p>
            </div>
            <div class="bg-blue-100 rounded-full p-3">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="card mb-8 animate-slide-up">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Acciones Rápidas</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button class="btn-primary flex items-center justify-center space-x-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            <span>Crear Nueva Ficha</span>
          </button>
          <button class="btn-secondary flex items-center justify-center space-x-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <span>Importar Masivo</span>
          </button>
          <button class="btn-secondary flex items-center justify-center space-x-2">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            <span>Exportar Catálogo</span>
          </button>
        </div>
      </div>

      <!-- API Status -->
      <div class="card animate-slide-up" style="animation-delay: 0.2s">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Estado del Sistema</h2>
        <div class="space-y-3">
          <div class="flex items-center justify-between py-2 border-b border-gray-100">
            <span class="text-sm text-gray-600">Backend API</span>
            <span :class="[apiConnected ? 'badge-success' : 'badge-critical', 'badge']">
              {{ apiConnected ? '✓ Conectado' : '✗ Desconectado' }}
            </span>
          </div>
          <div class="flex items-center justify-between py-2 border-b border-gray-100">
            <span class="text-sm text-gray-600">Base de Datos</span>
            <span :class="['badge-success', 'badge']">✓ Operativa</span>
          </div>
          <div class="flex items-center justify-between py-2">
            <span class="text-sm text-gray-600">Último Sync</span>
            <span class="text-sm text-gray-500">{{ lastSync }}</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const status = ref('Cargando...')
const apiConnected = ref(false)
const lastSync = ref('Nunca')
const stats = ref({
  products: 0,
  families: 0,
  languages: 6,
  compliance: 0
})

onMounted(async () => {
  try {
    // Check API connection
    const response = await api.get('/health')
    if (response.data.status === 'healthy') {
      apiConnected.value = true
      status.value = 'En línea'
      lastSync.value = new Date().toLocaleTimeString('es-ES')
      
      // Get stats
      const productsResponse = await api.get('/products')
      stats.value.products = productsResponse.data.total || 0
      stats.value.families = 3 // From presets
      stats.value.compliance = 85 // Example
    }
  } catch (error) {
    console.error('Error connecting to API:', error)
    status.value = 'Sin conexión'
    apiConnected.value = false
  }
})
</script>
