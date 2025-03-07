<template>
    <div class="container-fluid no-scroll">
      <div class="row h-100">
        <div class="col-md-6 col-12 d-flex flex-column h-100">
          <div class="login-card flex-grow-1 d-flex flex-column justify-content-between">
            <div class="centering-form">
              <div class="img-container">
                <img src="/icons/Logo.png" alt="logo-team-comunicaicones">
              </div>
              <div class="text-container">
                <h2>Bienvenid@ de nuevo</h2>
                <p>Ingresa tu usuario y contraseña para continuar.</p>
              </div>
              <form @submit.prevent="logineo">
                <div class="form-group">
                  <input type="text" name="username" class="form-control input_user" placeholder="Usuario" v-model.trim="form.username">
                </div>
                <div class="form-group">
                  <input type="password" name="password" class="form-control input_pass" placeholder="Contraseña" v-model.trim="form.password">
                </div>
                <!-- <div class="form-group d-flex justify-content-between align-items-center links-forgot">
                  <div class="d-flex align-items-center">
                    <input type="checkbox" class="form-check-input" id="rememberMe">
                    <label class="form-check-label ml-2" for="rememberMe">Recuérdame</label>
                  </div>
                  <a href="#" class="forgot-password">Olvidé mi contraseña</a>
                </div> -->
                <button type="submit" name="button" class="btn login_btn">Ingresar</button>
              </form>
            </div>
            <div class="cors mt-auto">
              <ul>
                <li>@2024 Team Comunicaciones S.A.S. Todos los derechos reservados</li>
                <li><a href="/politicas-privacidad">Política de privacidad</a>&nbsp;&nbsp;-&nbsp;&nbsp;<a href="/tratamiento-datos">Tratamiento de datos</a></li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-6 col-12 d-flex flex-column h-100">
          <div class="img-destacada">
            <img src="/img-example.jpg" alt="">
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import router from '../../../router'
  import Swal from 'sweetalert2'
  import backendRouter from '@/components/BackendRouter/BackendRouter'
  
  export default {
    data() {
      return {
        form: {
          username: '',
          password: '',
        },
      }
    },
    methods: {
      logineo() {
        const path = backendRouter.data + 'login'
        const access = {
          email: this.form.username,
          password: this.form.password,
        }
        axios.post(path, access).then((response) => {
          this.$cookies.set('jwt', response.data.jwt)
          router.push('/home')
        }).catch((error) => {
          Swal.fire({
            icon: 'error',
            title: 'Error de autenticación',
            text: 'Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.',
            customClass: {
              confirmButton: 'btn login_btn', 
            },
            buttonsStyling: false 
          })
        })
      },
    },
  }
  </script>