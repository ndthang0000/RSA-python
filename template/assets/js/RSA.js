class RSA {
    static randomPrime(bits) {
        const min = bigInt.one.shiftLeft(bits - 1);
        const max = bigInt.one.shiftLeft(bits).prev();
        
        while (true) {
        let p = bigInt.randBetween(min, max);
        if (p.isProbablePrime(256)) {
            return p;
        } 
        }
    }

    static generate(keysize,e_num) {
        //const e = e_num;
        const e = bigInt(e_num);
        let p;
        let q;
        let totient;
    
        do {
        p = this.randomPrime(keysize / 2);
        q = this.randomPrime(keysize / 2);
        
        //find phi= (p-1)(q-1)
        totient = bigInt.lcm(
            p.prev(), // p-1
            q.prev()  //q-1
        );
        } while (bigInt.gcd(e, totient).notEquals(1) || p.minus(q).abs().shiftRight(keysize / 2 - 100).isZero());

        return {
        e, 
        n: p.multiply(q),
        d: e.modInv(totient),
        };
    }

    static encrypt(encodedMsg, n, e) {
        return bigInt(encodedMsg).modPow(e, n);
    }

    static decrypt(encryptedMsg, d, n) {
        return bigInt(encryptedMsg).modPow(d, n); 
    }

    static encode(str) {
        const codes = str
        .split('')
        .map(i => i.charCodeAt())
        .join('');

        return bigInt(codes);
    }

    static decode(code) {
        const stringified = code.toString();
        let string = '';

        for (let i = 0; i < stringified.length; i += 2) {
        let num = Number(stringified.substr(i, 2));
        
        if (num <= 30) {
            string += String.fromCharCode(Number(stringified.substr(i, 3)));
            i++;
        } else {
            string += String.fromCharCode(num);
        }
        }

        return string;
    }
    }
function generateRSA(bit)
{   
    const keys = RSA.generate(bit,65537);
    return {
        d:keys.d.toString(),
        n:keys.n.toString(),
        e:65537,
    }
}
function decrypt(encrypted_message,d,n){
    const decrypted_message = RSA.decrypt(encrypted_message, d, n);
    const decoded_message = RSA.decode(decrypted_message);
    return decoded_message
}
function encrypt(message,n,e){
    const encoded_message = RSA.encode(message);
    const encrypted_message = RSA.encrypt(encoded_message, n, e);
    return encrypted_message
}
