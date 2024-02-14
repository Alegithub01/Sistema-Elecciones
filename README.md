# Sistema-Elecciones
Sprint 1 

## Si trabajara con su base de datos debe ingresar datos a sus tablas
 # tabla partido: insert into partido(nombre_partido,siglas) values("nombre_de_su_partido", "siglas_de_su_partido");
 # tabla persona: insert into partido(ci,nombres,ap_paterno,ap_materno,fecha_nacimiento,genero,direccion) values(15478595, "Juan Jose","Cossio","Cardenas",'1995-04-22','M',"Av. Heroinas");
 # tabla elector: insert into elector(ci_persona) values(15478595); //debe ser un ci registrado en persona
 # tabla candidato: insert into(ci_persona,id_partido,imagen_path) values(15478595, 1, "Cossio.jpg"); //debe existir el ci_persona y id_partido y de preferencia ponga en la ruta de imagen el ap_paterno del candidato con la exetencion jpg.  
 #  tabla tribunal: insert into tribunal(username,password) values("su_usario","su_contrasenia");

 # ACLARACION si agregara mas candidato debe nombre a la imagen como el ap_paterno de su candidato  con la extencion jpg "Cossio.jpg" y guardarlo en la ruta /static/img/

# Si desea trabajar con los datos que ya existen en la base de datos ya proporcionados en el host estos usuarios son electores habilitados:
1 ci: 65165 fecha nacimiento: 22/07/1982
2 ci: 5551635 fecha nacimiento: 22/07/1975
3 ci: 2587455 fecha nacimiento: 22/07/1952


