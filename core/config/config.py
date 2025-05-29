config = {
    "hosts":{
         "camera":"192.168.0.20",
         "database":"localhost",
    },

    "ports":{
         "camera":80,
         "database":3306,
    },
    
    "credentials":{
         "database": {
             "user":"root",
             "password":"@Isac1998",
             "name":"debug"
         }
    },
    
    "details":{
         "camera": {
             "resolution":"800x600",
             "format":"JPG"
         },

         "database":{
             "tables":{   
                 "perfis":{
                    "name":"usuarios",
                    "columns":["nome", "email", "alias", "matricula", "id"],
                    "password_column":"senha",
                    "encoding_column":"encodings",
                    "trust":60
                 },

                 "historico":{
                    "name":"historico",
                 },

                 "devices":{
                    "name":"dispositivos",
                 }

             }
         }
    },
}