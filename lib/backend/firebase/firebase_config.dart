import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

Future initFirebase() async {
  if (kIsWeb) {
    await Firebase.initializeApp(
        options: const FirebaseOptions(
            apiKey: "AIzaSyBofx7xcZZc6Ky9MkFzRLujJa2wONKpFF4",
            authDomain: "mux-starter-ldo0e8.firebaseapp.com",
            projectId: "mux-starter-ldo0e8",
            storageBucket: "mux-starter-ldo0e8.appspot.com",
            messagingSenderId: "810159114511",
            appId: "1:810159114511:web:fc001438760b85b396167a"));
  } else {
    await Firebase.initializeApp();
  }
}
