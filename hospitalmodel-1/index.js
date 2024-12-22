// Import Three.js and GLTFLoader
import * as THREE from './three.module.js';
import { GLTFLoader } from './examples/js/loaders/GLTFLoader.js';

// Scene, Camera, Renderer setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Add a Light
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 10, 7.5);
scene.add(light);

// Load the GLB model
const loader = new GLTFLoader();
loader.load(
  'Hospital OR 1.glb', // Path to your GLB file
  (gltf) => {
    const model = gltf.scene; // Access the loaded scene
    scene.add(model); // Add the model to the scene
    model.position.set(0, 0, 0); // Position the model
  },
  (xhr) => {
    console.log(`Model ${(xhr.loaded / xhr.total) * 100}% loaded`);
  },
  (error) => {
    console.error('An error occurred while loading the model', error);
  }
);

// Set the camera position
camera.position.z = 5;

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
animate();

// Resize listener
window.addEventListener('resize', () => {
  renderer.setSize(window.innerWidth, window.innerHeight);
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
});
