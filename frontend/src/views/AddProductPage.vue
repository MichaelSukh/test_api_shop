<template>
  <div class="add-product-container">
    <div class="card">
      <h2>Добавить новый товар</h2>
      
      <form @submit.prevent="submitForm" class="add-product-form">
        <div class="form-group">
          <label for="name">Название товара <span class="required">*</span></label>
          <input 
            type="text" 
            id="name" 
            v-model="productForm.name" 
            required 
            placeholder="Введите название"
          />
        </div>

        <div class="form-group">
          <label for="description">Описание</label>
          <textarea 
            id="description" 
            v-model="productForm.description" 
            rows="4" 
            placeholder="Опишите товар"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="price">Цена <span class="required">*</span></label>
          <input 
            type="number" 
            id="price" 
            v-model.number="productForm.price" 
            required 
            min="0"
            step="0.01"
            placeholder="0.00"
          />
        </div>

        <div class="form-group">
          <label for="image_url">URL изображения</label>
          <input 
            type="url" 
            id="image_url" 
            v-model="productForm.image_url" 
            placeholder="https://example.com/image.jpg"
          />
        </div>

        <div class="form-group">
          <label for="category">Категория <span class="required">*</span></label>
          <select 
            id="category" 
            v-model="productForm.category_id" 
            required
          >
            <option disabled :value="null">Выберите категорию</option>
            <option 
              v-for="category in store.categories" 
              :key="category.id" 
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <button 
          type="submit" 
          class="submit-button" 
          :disabled="store.loading"
        >
          <span v-if="store.loading">Отправка...</span>
          <span v-else>Сохранить товар</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProductsStore } from '@/stores/products'

const store = useProductsStore()
const router = useRouter()

const productForm = reactive({
  name: '',
  description: '',
  price: null,
  image_url: '',
  category_id: null
})

const errorMessage = ref('')

onMounted(async () => {
  try {
    await store.fetchCategories()
  } catch (error) {
    console.error('Ошибка при загрузке категорий:', error)
    errorMessage.value = 'Не удалось загрузить категории'
  }
})

const submitForm = async () => {
  errorMessage.value = ''
  try {
    await store.createProduct(productForm)
    router.push('/')
  } catch (error) {
    console.error('Ошибка при добавлении товара:', error)
    errorMessage.value = error.message || 'Произошла ошибка при сохранении товара.'
  }
}
</script>

<style scoped>
.add-product-container {
  display: flex;
  justify-content: center;
  padding: 2rem;
  background-color: #f9fafb;
  min-height: calc(100vh - 100px);
}

.card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  width: 100%;
  max-width: 500px;
}

h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #111827;
  font-size: 1.5rem;
  font-weight: 600;
  text-align: center;
}

.add-product-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.required {
  color: #ef4444;
}

input,
textarea,
select {
  padding: 0.625rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
  color: #111827;
  background-color: #fff;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

textarea {
  resize: vertical;
}

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  background-color: #fef2f2;
  padding: 0.75rem;
  border-radius: 6px;
  border: 1px solid #fecaca;
}

.submit-button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
  display: flex;
  justify-content: center;
  align-items: center;
}

.submit-button:hover:not(:disabled) {
  background-color: #2563eb;
}

.submit-button:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}
</style>
