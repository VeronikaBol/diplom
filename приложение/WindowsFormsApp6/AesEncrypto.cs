using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace WindowsFormsApp6
{



    class AES
    {




        //зашифрование
    public static byte[] encrypt(string fileName)
    {

            Aes myAes = Aes.Create();
            byte[] encrypted = encrypt(fileName, myAes.Key, myAes.IV);
            File.WriteAllBytes("key_tmp.key", myAes.Key);
            
            return encrypted;
    }
    //расшифрование

    public static byte[] decrypt(string fileName, byte[] key)
        {
            Aes myAes = Aes.Create();
            myAes.Key = key;
            return decrypt(File.ReadAllBytes(fileName),key, myAes.IV);
        }



        static byte[] encrypt(string fileName, byte[] Key, byte[] IV)
    {
       

        if (Key == null || Key.Length <= 0)
            throw new ArgumentNullException("Key");
        if (IV == null || IV.Length <= 0)
            throw new ArgumentNullException("IV");
        byte[] encrypted;


        using (Aes aesAlg = Aes.Create())
        {
            aesAlg.Key = Key;
            aesAlg.IV = IV;


            ICryptoTransform encryptor = aesAlg.CreateEncryptor(aesAlg.Key, aesAlg.IV);


            using (MemoryStream msEncrypt = new MemoryStream())
            {
                using (CryptoStream csEncrypt = new CryptoStream(msEncrypt, encryptor, CryptoStreamMode.Write))
                {
                    using (StreamWriter swEncrypt = new StreamWriter(csEncrypt))
                    {
                      
                        swEncrypt.Write(fileName);
                    }
                    encrypted = msEncrypt.ToArray();
                }
            }
        }

      
        return encrypted;
    }

    static byte[] decrypt(byte[] cipherText, byte[] Key, byte[] IV)
    {
        // Check arguments.
        if (cipherText == null || cipherText.Length <= 0)
            throw new ArgumentNullException("cipherText");
        if (Key == null || Key.Length <= 0)
            throw new ArgumentNullException("Key");
        if (IV == null || IV.Length <= 0)
            throw new ArgumentNullException("IV");

        // Declare the string used to hold
        // the decrypted text.
        string plaintext = null;
            byte[] result = new byte[0];
            // Create an Aes object
            // with the specified key and IV.
            using (Aes aesAlg = Aes.Create())
        {
            aesAlg.Key = Key;
            aesAlg.IV = IV;
               
            // Create a decryptor to perform the stream transform.
            ICryptoTransform decryptor = aesAlg.CreateDecryptor(aesAlg.Key, aesAlg.IV);

            // Create the streams used for decryption.
            using (MemoryStream msDecrypt = new MemoryStream(cipherText))
            {
                using (CryptoStream csDecrypt = new CryptoStream(msDecrypt, decryptor, CryptoStreamMode.Read))
                {
                    using (StreamReader srDecrypt = new StreamReader(csDecrypt))
                    {

                        // Read the decrypted bytes from the decrypting stream
                        // and place them in a string.
                        plaintext = srDecrypt.ReadToEnd();
                    }
                }
                    result = msDecrypt.ToArray();
            }
        }

        return result;
    }
}



    class RSA
    {
        public static string encrypt(string key, string keysDH)
        {
            List<string> keys = new List<string>();

            return keys[0];
        }

        public static byte[] decrypt(string AESkey, string key)
        {
            List<byte> keyByte = new List<byte>();
            return keyByte.ToArray();
        }
    }
}
