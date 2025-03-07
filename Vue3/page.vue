<template >
    <div >
        <MenuLanding/>
        <Carrito ref="carrito"/>
        <BCarousel controls>
            <BCarouselSlide  :img-src="getImageUrl('slide1.png')" />
            <BCarouselSlide  :img-src="getImageUrl('slide2.png')" />
        </BCarousel>
        <div id="'portafolio'" class="row portafolio m-5">
            <a :class="{'clase-activa col-4': portafolio.var, 'clase-inactiva col-4': !portafolio.var}" v-for="portafolio in portafolios" href="#" :key="portafolio.id" style="text-decoration:none; color: black;">
                <img
                :src="getImageUrl(portafolio.img)" 
                @mouseover="zoomIn(portafolio.id)"
                @mouseout="zoomOut(portafolio.id)"
                style="width: 120px; height: 60px;"/>
            </a>
        </div>
        <div id="planes">
            <VueHorizontal class="p-3" style="align-items: end;">
                <section v-for="plan in planes" :key="plan.id" class="m-4">
                    <a href="#" style="text-decoration:none; color: black;">
                        <img
                        v-bind:src="getImageUrl(plan.img)" 
                        style="width: 200px; height: 200px;"/>
                    </a>
                </section>
            </VueHorizontal>
        </div>
        <div id="planes_prepago">
            <BButton to="/tienda" class="m-4" variant="danger">Adquiere tu plan pospago ahora</BButton>
        </div>
        <BCarousel controls>
            <BCarouselSlide  :img-src="getImageUrl('slide3.png')" />
            <BCarouselSlide  :img-src="getImageUrl('slide4.jpg')" />
            <BCarouselSlide  :img-src="getImageUrl('slide5.jpg')" />
        </BCarousel>
        
        <div id="productos">
            <VueHorizontal class="p-3" style="align-items: end;">
                <section v-for="producto in productos" :key="producto.id" class="m-4">
                    <a href="#" style="text-decoration:none; color: black;">
                        <img
                        :src="getImageUrl(producto.img)" 
                        style="width: 200px; height: 320px;"/>
                        <h5>{{ producto.name }}</h5>
                        <p style="color: red;">{{ formatoMoneda(producto.value) }} iva incluido</p>
                    </a>
                    <BButton class="m-4" variant="danger" @click="agregarAlCarrito(producto)">Agregar al carrito</BButton>
                </section>
            </VueHorizontal>
        </div>
    </div>
    
  </template>
  
  <script>
    import VueHorizontal from 'vue-horizontal';
    import MenuLanding from '../MenuLanding/MenuLanding.vue'
    import Carrito from '@/components/MainPage/Carrito/Carrito.vue'
    import backendRouter from '@/components/BackendRouter/BackendRouter';
    import axios from 'axios';
    import {ref} from 'vue'
  export default{
    data(){
        return{
            imagenP: '../../../assets/asiSomos/complementaria.jpeg',
            slide: 0,
            slide2: 0,
            sliding: null,
            slidesData:[
                {id:1, caption:'', text:'', img:'slide1.png'},
                {id:1, caption:'', text:'', img:'slide2.jpg'},
                {id:1, caption:'', text:'', img:'slide3.jpg'},
            ],
            slidesData2:[
                {id:1, caption:'', text:'', img:'slide1.png'},
                {id:1, caption:'', text:'', img:'slide2.png'},
            ],
            portafolios:[
                {id:1, img:'portafolio1.jpg', var:false},
                {id:2, img:'portafolio2.jpg', var:false},
                {id:3, img:'portafolio3.jpg', var:false},
            ],
            planes:[],
            productos:[],
        }
    },
    components:{  
        VueHorizontal,
        MenuLanding,
        Carrito,
    },
    setup(){
        const getImageUrl = (name) => {
            var nombreUrl = 'logo.png'
            return new URL(`../../../assets/${name}`, import.meta.url).href
        }
        return {getImageUrl }
    },
    methods: {
        formatoMoneda(valor) {
            const resultado = parseFloat(valor).toLocaleString('es-CO', {
                style: 'currency',
                currency: 'COP',
            })
            return resultado
        },
        zoomIn(num) {
            this.portafolios[num-1].var = true;
        },
        zoomOut(num) {
            this.portafolios[num-1].var = false;
        },
        getPlanes(){
            
            // this.planes.push({ id: 1, img: '@/assets/planes/plan1.jpg'});
            const path = backendRouter.data+'planes'
            axios.get(path).then((response)=>{
                
                response.data.data.map(plan =>{
                    
                    // plan.img = require(`@/assets/planes/${plan.img}`)
                    this.planes.push({id:plan.id, img: plan.img})
                    
                })
               
                
            })
        },
        getProductos(){
            
            // this.planes.push({ id: 1, img: '@/assets/planes/plan1.jpg'});
            const path = backendRouter.data+'productos'
            axios.get(path).then((response)=>{
                
                response.data.data.map(plan =>{
                    
                    // plan.img = new URL(`@/assets/productos/${plan.img}`, import.meta.url).href
                    this.productos.push({id:plan.id, img: plan.img, name:plan.titulo, value:plan.precio})
                })
                
                
            })
        },
        agregarAlCarrito: function(producto) {
            // Emite el evento 'agregar-al-carrito' con los detalles del producto
            // console.log('inicio bus')
            // console.log(producto)
            this.$refs.carrito.agregarAlCarritoCarrito(producto)
        },
    },
    created(){
        this.getPlanes()
        this.getProductos()
    }, 
  }
  </script>
  
  <style scoped>
    .red{
        background-color: red;
    }
    .contactos_container{
        border-color: black;
        border-radius: 5px;
    }
    .portafolio{
        text-align: center;
    }
    .clase-activa{
        transform: scale(1.5);
        z-index: 999;
    }
    .clase-inactiva{
        transform: scale(1)
    }
  
  </style>
