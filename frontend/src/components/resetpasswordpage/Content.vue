<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from "vue-router"
import { useNotification } from "@kyvg/vue3-notification"

const notification = useNotification()
const router = useRouter()

// Form states
const email = ref('')
const otp = ref('')
const password = ref({
  pass: '',
  confirmPass: ''
})

// UI states
const formStep = ref('email') // 'email', 'otp', 'password'
const isLoading = ref(false)
const errors = ref({
  email: '',
  otp: '',
  password: ''
})

// To store the interval ID for clearing
const countdown = ref(120)
let countdownInterval = null

// handle 2 button "deactive" css, resend otp
const isResending = ref(false)

// Validation functions
const validateEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
const validatePassword = (password) => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,20}$/.test(password)
const validateOtp = (otp) => /^\d{6}$/.test(otp)


// Email submission
async function handleEmailSubmit() {
  errors.value.email = ''

  if (!validateEmail(email.value)) {
    errors.value.email = 'Please enter a valid email address.'
    return
  }

  try {
    isLoading.value = true
    const response = await axios.post('users/reset-password/', {
      email: email.value
    })

    if (response.data.message) {
      formStep.value = 'otp'
      notification.notify({
          title: "OTP Sent",
          text: "Check your email for the verification code."
        })
        // Start the OTP countdown
      startCountdown()
    }
  } catch (err) {
    errors.value.email = "Failed to send OTP. Please try again."
  } finally {
    isLoading.value = false
  }
}



// OTP verification
async function handleOtpSubmit() {
  errors.value.otp = ''

  if (!validateOtp(otp.value)) {
    errors.value.otp = 'Please enter a valid 6-digit code.'
    return
  }

  try {
    isLoading.value = true
    const response = await axios.post("users/verify-reset-otp/", {
      email: email.value,
      otp: otp.value
    })

    // success otp clear clearInterval
    if (response.data.message) {
      formStep.value = 'password'
      clearInterval(countdownInterval)
    } else {
      errors.value.otp = "Network error. Please try again."
    }
  } catch (err) {
    errors.value.otp = "Invalid OTP. Please try again."
  } finally {
    isLoading.value = false
  }
}



// Password submission
async function handlePasswordSubmit() {
  errors.value.password = ''

  if (!validatePassword(password.value.pass)) {
    errors.value.password = 'Password must be 8-20 characters with uppercase, lowercase, and number.'
    return
  }

  if (password.value.pass !== password.value.confirmPass) {
    errors.value.password = "Passwords don't match."
    return
  }

  try {
    isLoading.value = true
    const response = await axios.post("users/new-password/", {
      email: email.value,
      otp: otp.value,
      pass: password.value.pass
    })

    if (response.data.message) {
      notification.notify({
        title: "Success!",
        text: "Password changed successfully."
      })
      router.push("/log-in")
    }
  } catch (err) {
    errors.value.password = "Failed to update password. Please try again."
  } finally {
    isLoading.value = false
  }
}


// Resends the OTP code
async function resendCode() {
  // Reset countdown and clear previous interval
  clearInterval(countdownInterval)

  // Reset countdown to 2 minutes
  countdown.value = 120

  // Set resending specific loading state
  isResending.value = true
  try {
    // Re-trigger the initial email submission to send a new OTP
    await handleEmailSubmit()
  } finally {
    isResending.value = false
  }
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
    <!-- Email Step -->
    <form @submit.prevent="handleEmailSubmit" v-if="formStep === 'email'">
      <h4>Reset Your Password</h4>
      <input type="email" v-model.trim="email" placeholder="Your Email" required :disabled="isLoading" />
      <span v-if="errors.email">● {{ errors.email }}</span>
      <button type="submit" :class="{ 'deactive' : isLoading }" :disabled="isLoading">
        {{ isLoading ? 'Sending...' : 'Send OTP' }}
      </button>
    </form>
    <!-- OTP Step -->
    <form @submit.prevent="handleOtpSubmit" v-else-if="formStep === 'otp'">
      <h4>Enter Verification Code</h4>
      <input type="text" v-model.trim="otp" placeholder="6-digit code" required :disabled="isLoading || isResending" />
      <span v-if="errors.otp">● {{ errors.otp }}</span>
      <button type="submit" :class="{ 'deactive' : isLoading && !isResending }" :disabled="isLoading || isResending">
        {{ isLoading ? 'Verifying...' : 'Verify Code' }}
      </button>
      <button type="button" class="resend-btn" @click="resendCode" :class="{ 'deactive': isResending }" :disabled="countdown > 0 || isLoading || isResending">
        Resend Code {{ countdown > 0 ? `(${countdown})` : '' }}
      </button>
    </form>
    <!-- Password Step -->
    <form @submit.prevent="handlePasswordSubmit" v-else>
      <h4>Set New Password</h4>
      <input type="password" v-model.trim="password.pass" placeholder="New Password" required :disabled="isLoading" />
      <input type="password" v-model.trim="password.confirmPass" placeholder="Confirm Password" required :disabled="isLoading" />
      <span v-if="errors.password">● {{ errors.password }}</span>
      <button type="submit" :class="{ 'deactive' : isLoading }" :disabled="isLoading">
        {{ isLoading ? 'Updating...' : 'Update Password' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.form {
  background-color: var(--secondary-black);
  width: 350px;
  padding: 30px;
  border-radius: 5px;
  display: flex;
  flex-direction: column;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

input {
  color: #fff;
  border: 0;
  border-radius: 3px;
  width: 100%;
  padding: 10px 15px;
  background-color: var(--tertiary-black);
}

input:focus-visible {
  outline: none;
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

span {
  color: red;
  font-size: 12px;
  margin-top: -10px;
  padding-left: 5px;
}

h4 {
  color: #fff;
  text-align: center;
  margin-bottom: 15px;
}

.deactive {
  animation: btn-bg 1s infinite;
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
