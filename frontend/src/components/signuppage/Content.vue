<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useNotification } from "@kyvg/vue3-notification"

const notification = useNotification()
const router = useRouter()

// Form states
const submitValues = ref({
  name: "",
  email: "",
  password: "",
  otp: ""
})

// UI states
const formStep = ref('signup') // 'signup', 'otp'
const isLoading = ref(false)
const errors = ref({
  name: '',
  email: '',
  password: '',
  otp: '',
  general: ''
})
const countdown = ref(120)

// To store the interval ID for clearing
let countdownInterval = null


// Allows alphanumeric characters, underscores, spaces, and hyphens.
// Length must be between 3 and 25 characters.
const validateName = (name) => /^[a-zA-Z0-9_\s-]{3,25}$/.test(name)

// Follows a standard email format
// Does not allow leading/trailing spaces or spaces within the local part or domain.
const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)

// Requires at least one lowercase letter.
// Requires at least one uppercase letter.
// Requires at least one digit.
// Length must be between 8 and 20 characters.
// Only allows alphanumeric characters.
const validatePassword = (password) => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,20}$/.test(password)

// Must consist of exactly 6 digits.
const validateOtp = (otp) => /^\d{6}$/.test(otp)



// Handles initial sign-up form submission
async function handleSignUpSubmit() {
  // Clear all previous errors
  errors.value = { name: '', email: '', password: '', otp: '', general: '' }

  let hasError = false

  // Validate all fields
  if (!validateName(submitValues.value.name)) {
    errors.value.name = 'Only 3 - 25 characters allowed (a-Z, 0-9, _, -, space).'
    hasError = true
  }
  if (!validateEmail(submitValues.value.email)) {
    errors.value.email = 'Please enter a valid email address.'
    hasError = true
  }
  if (!validatePassword(submitValues.value.password)) {
    errors.value.password = 'Password must be 8-20 characters with lowercase, uppercase, and digit.'
    hasError = true
  }

  // validation fails, stop submission
  if (hasError) {
    return
  }

  try {
    isLoading.value = true
    const response = await axios.post('users/sign-up/', submitValues.value)

    if (response.data.message) {
      formStep.value = 'otp' // Move to OTP verification step
      notification.notify({
          title: "Please verify OTP.",
          text: "A 6-digit code has been sent to your email."
        })
        // Start the OTP countdown
      startCountdown()
    }
  } catch (err) {
    // Handle specific API errors
    if (err.response) {

      if (err.response.status === 409) {
        // name Conflict
        if (err.response.data.nameStatus) {
          errors.value.name = err.response.data.nameStatus
        }

        // email conflict
        if (err.response.data.emailStatus) {
          errors.value.email = err.response.data.emailStatus
        }

        // Server error or OTP sending failure
      } else if (err.response.status === 500) {
        errors.value.general = "Failed to send OTP. Please try again."
        notification.notify({
          title: "OTP Send Failed.",
          text: "Please try submitting the form again."
        })
      } else {
        errors.value.general = "An unexpected error occurred. Please try again."
      }
    } else {
      // Network error or no response from server
      errors.value.general = "Network error. Please try again."
    }
  } finally {
    isLoading.value = false
  }
}



// Handles OTP verification form submission
async function handleOtpSubmit() {
  errors.value.otp = '' // Clear previous OTP error

  if (!validateOtp(submitValues.value.otp)) {
    errors.value.otp = 'Please enter a valid 6-digit code.'
    return
  }

  isLoading.value = true
  try {
    const response = await axios.post('users/verify/', submitValues.value)

    if (response.status === 200) {
      notification.notify({
          title: "Account Created 🎉",
          text: "Now you can log in."
        })
        // Redirect to login page on success
      router.push('/log-in')
    }
  } catch (err) {
    if (err.response) {
      errors.value.otp = "Invalid OTP. Please try again."
    } else {
      errors.value.otp = "Network error. Please try again."
    }
  } finally {
    isLoading.value = false
  }
}



// Resends the OTP code
async function resendCode() {
  // Reset OTP input and error
  submitValues.value.otp = ''
  errors.value.otp = ''

  // Reset countdown and clear previous interval
  clearInterval(countdownInterval)
  countdown.value = 120

  // Re-trigger the initial sign-up process to send a new OTP
  // for existing but unverified emails.
  await handleSignUpSubmit()
}

// Starts the countdown timer for OTP
function startCountdown() {
  if (countdownInterval) {
    // Clear any existing interval
    clearInterval(countdownInterval)
  }
  countdownInterval = setInterval(() => {
    countdown.value--
      if (countdown.value <= 0) {
        clearInterval(countdownInterval)
      }
  }, 1000)
}
</script>
<template>
  <div class="form">
    <!-- user form -->
    <form @submit.prevent="handleSignUpSubmit" v-if="formStep === 'signup'">
      <h4>Create Account</h4>
      <input type="text" v-model.trim="submitValues.name" placeholder="Your Name" required :disabled="isLoading" />
      <span v-if="errors.name">● {{ errors.name }}</span>
      <input type="email" v-model.trim="submitValues.email" placeholder="Your Email" required :disabled="isLoading" />
      <span v-if="errors.email">● {{ errors.email }}</span>
      <input type="password" v-model.trim="submitValues.password" placeholder="Password" required :disabled="isLoading" />
      <span v-if="errors.password">● {{ errors.password }}</span>
      <span v-if="errors.general">● {{ errors.general }}</span>
      <button type="submit" :class="{ 'deactive': isLoading }" :disabled="isLoading">
        {{ isLoading ? 'Submitting...' : 'Sign Up' }}
      </button>
    </form>
    <!-- otp form -->
    <form @submit.prevent="handleOtpSubmit" v-else-if="formStep === 'otp'">
      <h4>Please enter the OTP from your email</h4>
      <input type="text" v-model.trim="submitValues.otp" placeholder="6-digit code" required :disabled="isLoading" />
      <span v-if="errors.otp">● {{ errors.otp }}</span>
      <button type="submit" :class="{ 'deactive': isLoading }" :disabled="isLoading">
        {{ isLoading ? 'Verifying...' : 'Verify' }}
      </button>
      <button type="button" class="resend-btn" @click="resendCode" :class="{ 'deactive': isLoading }" :disabled="countdown > 0 || isLoading">
        Resend Code {{ countdown > 0 ? `(${countdown})` : '' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  border-radius: 5px;
  padding: 30px;
  width: 350px;
  background-color: var(--secondary-black);
}

form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 15px;
}

input {
  color: #fff;
  border: 0;
  border-radius: 3px;
  width: 100%;
  padding: 10px 15px 10px 15px;
  background-color: var(--tertiary-black);
}

input:focus-visible {
  outline: none;
  color: #fff;
}

button {
  border: 0;
  background-color: var(--accent);
  border-radius: 25px;
  padding: 9px;
  color: #fff;
  cursor: pointer;
}

button:disabled {
  background-color: var(--tertiary-black);
  cursor: not-allowed;
}

.resend-btn {
  background-color: var(--tertiary-black);
}

.deactive {
  animation: btn-bg 1s infinite;
}

span {
  color: red;
  padding-left: 5px;
  margin-top: -10px;
  font-size: 12px;
  font-weight: 400;
}

h4 {
  color: #fff;
  text-align: center;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 15px;
}

@keyframes btn-bg {
  0% {
    background-color: var(--tertiary-black);
  }
  50% {
    background-color: rgb(145 145 145 / 64%);
  }
  100% {
    background-color: var(--tertiary-black);
  }
}
</style>
