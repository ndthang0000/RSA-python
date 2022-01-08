import RSA from './index.js'

function RSAtoAES(bit,message)
{   
    
    //import RSA from './index.js' 
    //const RSA = require('.');

    // Messageno
    //const message = 'secret key 123 ';

    // Generate RSA keys
    const keys = RSA.generate(bit,65537);// length of bits, public key e

    console.log('Keys');
    console.log('n:', keys.n.toString());
    console.log('d:', keys.d.toString());
    console.log('e:', keys.e.toString());


    const encoded_message = RSA.encode(message);
    const encrypted_message = RSA.encrypt(encoded_message, keys.n, keys.e);
    const decrypted_message = RSA.decrypt(encrypted_message, keys.d, keys.n);
    const decoded_message = RSA.decode(decrypted_message);
    console.log(decrypted_message)

    console.log('Message:', message);
    console.log('Encoded:', encoded_message.toString());
    console.log('Encrypted:', encrypted_message.toString());
    console.log('Decrypted:', decrypted_message.toString());
    console.log('Decoded:', decoded_message.toString());
    console.log();
    console.log('Correct?', message === decoded_message);
    return encrypted_message 
}
const message = 'secret key 123 ';
result = RSAtoAES(1024,message)
console.log('Encrypted:', result.toString());

export default RSAtoAES;




