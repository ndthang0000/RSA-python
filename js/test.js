require('./example.js');
import {RSAtoAES} from  './example.js'
//import { RSAtoAES } from "./example.js";

const message = 'secret key 123 ';
result = RSAtoAES(1024,message)
console.log('Encrypted:', result.toString());