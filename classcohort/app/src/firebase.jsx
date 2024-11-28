// Import the functions you need from the SDKs
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDt4x4HISpIB94H9afClO_OyzG1uc7kO54",
  authDomain: "bank-3028e.firebaseapp.com",
  projectId: "bank-3028e",
  storageBucket: "bank-3028e.appspot.com",
  messagingSenderId: "895853053447",
  appId: "1:895853053447:web:0e58f5408b92c9f76acca2",
  measurementId: "G-2VHC1ZE4KR",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Authentication
const auth = getAuth(app);

// Firestore
const db = getFirestore(app);

export { auth, db };
