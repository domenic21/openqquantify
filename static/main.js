//Import the THREE.js library
import * as THREE from "https://cdn.skypack.dev/three@0.129.0/build/three.module.js";
// To allow for the camera to move around the scene
import { OrbitControls } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/controls/OrbitControls.js";
// To allow for importing the .gltf file
import { GLTFLoader } from "https://cdn.skypack.dev/three@0.129.0/examples/jsm/loaders/GLTFLoader.js";

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

//object in a global variable to access
let object;

//for camera controls
let controls;

//for render
let objToRender = 'computer';



const loader = new GLTFLoader();

//track mouse movement
let mouseX = window.innerWidth / 2;
let mouseY = window.innerHeight / 2;

loader.load(
    '/static/computer/scene.gltf',
    function (gltf) {
        object = gltf.scene;
        object.scale.set(15, 10, 25); // is x 0.1, y 0.1, z 0.1 , z means depth
        scene.add(object);
    },
    function (xhr) {
        console.log((xhr.loaded / xhr.total * 100) + '% loaded');
    },
    function (error) {
        console.error('An error happened', error);
    }
);

//init render and set size
const renderer = new THREE.WebGLRenderer({ alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
const container = document.getElementById('container3d');
if (container) {
    container.appendChild(renderer.domElement);
} else {
    console.error("Element with id 'container3d' not found in the DOM.");
}
//set camera position
camera.position.z = objToRender === 'computer' ? 25 : 500;

//add lights 
const toplight = new THREE.DirectionalLight(0xffffff, 1);
toplight.position.set(0, 100, 0);
toplight.castShadow = true;
scene.add(toplight);

const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);
//orbit controls 
if (objToRender === 'computer') {
     controls = new OrbitControls(camera, renderer.domElement);
}

//render scene
function animate(){
    requestAnimationFrame(animate);
    
    if(object && objToRender === 'computer') {
        object.rotation.y = -3 + mouseX / window.innerWidth * 3;
        object.rotation.x = -1.2 + mouseY * 2.5 / window.innerHeight ;
    }
    renderer.render(scene, camera);

}

//add listener to the window so we can resize the camera 
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

//add mouse move listener
window.addEventListener('mousemove', (event) => {
    mouseX = event.clientX;
    mouseY = event.clientY;
});

animate();