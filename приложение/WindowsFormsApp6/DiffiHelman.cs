﻿using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace WindowsFormsApp6
{
    class DH
    {
        //сформировать свой ключ
        public static string getPersonalKey()
        {
            if (!File.Exists("DH_KEYS.data"))
            {
                using (ECDiffieHellmanCng alice = new ECDiffieHellmanCng())
                {

                    alice.KeyDerivationFunction = ECDiffieHellmanKeyDerivationFunction.Hash;
                    alice.HashAlgorithm = CngAlgorithm.Sha256;
                    byte[] bobPublicKey = alice.PublicKey.ToByteArray();
                    File.WriteAllBytes("DH_KEYS.data", bobPublicKey);
                }
            }

            return "";
        }

        //сформировать ключи для всех остальных пользователей
        public static string getKeys(string token)
        {


            List<byte[]> keys = new List<byte[]>();
            List<string> result = new List<string>();
            ECDiffieHellmanCng alice = new ECDiffieHellmanCng();
            

                alice.KeyDerivationFunction = ECDiffieHellmanKeyDerivationFunction.Hash;
                alice.HashAlgorithm = CngAlgorithm.Sha256;
                


                
           
                    CngKey bobKey = CngKey.Import(Encoding.UTF8.GetBytes(token), CngKeyBlobFormat.EccPublicBlob);

            return Encoding.UTF8.GetString(alice.DeriveKeyMaterial(bobKey));
                           
                
                
            



        }
    }
}
